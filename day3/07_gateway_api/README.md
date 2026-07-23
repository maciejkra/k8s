# 07 — Gateway API (Envoy Gateway)

Następca **Ingress**. Ingress jest dziś legacy — routing po hoście/ścieżce, a wszystko
inne (rewrite, TLS, nagłówki) przez adnotacje specyficzne dla kontrolera ("annotation
hell"). Gateway API (GA od v1.0 w 2023, dziś v1.6 — osobny projekt, wersjonowany
niezależnie od Kubernetesa) robi to deklaratywnie, w typowanych obiektach:

| Obiekt         | Co opisuje                                   | Odpowiednik w Ingress |
|----------------|----------------------------------------------|-----------------------|
| `GatewayClass` | KTÓRA implementacja (Envoy, NGINX, Cilium…)  | `IngressClass`        |
| `Gateway`      | instancja LB: porty i listenery (80/443)     | część `Ingress`       |
| `HTTPRoute`    | reguły routingu (host, path, filtry)         | `rules:` w `Ingress`  |

Backendy: `nginx` + `echo-server` z `backends.yaml` — bez zależności od innych dni.

## Wymagania

Klaster: **kind** (`workshop` z `day2/04_k8s/kind.yaml`) albo **Docker Desktop**
z włączonym Kubernetesem.

> Porty `:80`/`:443` muszą być wolne na hoście — sprawdź `sudo lsof -nP -iTCP:80 -sTCP:LISTEN`.

Do **Przykładu 4C** (Let's Encrypt) potrzebny jest klaster w chmurze z publicznym IP —
lokalnie się nie da. Na DigitalOcean (DOKS) **pomiń instalację z Kroku 1** i użyj
wbudowanego Cilium — patrz callout niżej oraz Przykład 4C.

---

## Krok 1 — Instalacja Envoy Gateway (bez Helma)

Helm poznajemy dopiero w `day5/05_helm`, więc tu zwykły `kubectl apply`:

```sh
kubectl apply --server-side -f https://github.com/envoyproxy/gateway/releases/download/v1.8.2/install.yaml

kubectl wait --timeout=180s -n envoy-gateway-system \
  deployment/envoy-gateway --for=condition=Available
```

`install.yaml` zawiera CRD-y Gateway API + Envoy Gateway. **Nie** tworzy `GatewayClass`
— robi to `gateway-http.yaml` w Kroku 3.

### Na klastrze zarządzanym (DigitalOcean/DOKS) — nie instaluj Envoy

DOKS ma wbudowany Cilium z włączonym Gateway API, więc kontrolera **nie instalujesz w ogóle** —
`GatewayClass cilium` jest gotowa (`kubectl get gatewayclass` → `cilium  ...  Accepted  True`).
Instalacja z Kroku 1 tam zresztą **padnie**: DOKS sam zarządza CRD-ami Gateway API (pin na
starszą wersję, field manager `c3`), więc każdy instalator z własnymi CRD-ami Gateway API zderza
się z `Apply failed ... conflicts with "c3"`.

Dlatego na DOKS **pomiń Kroki 1–3**. Zamiast `GatewayClass eg` + `gateway-http.yaml` użyj Gatewaya
z `gatewayClassName: cilium` — DO sam nada mu publiczny `EXTERNAL-IP` (Service `cilium-gateway-<nazwa>`).
Pełny, przetestowany przepis (HTTP → Let's Encrypt → HTTPS) jest w **Przykładzie 4C**.

---

## Krok 2 — Ekspozycja na hoście

**Docker Desktop** — nic nie trzeba. Wbudowany LoadBalancer nada Service'owi Envoya
`EXTERNAL-IP: localhost`. Pomiń resztę tego kroku oraz `kubectl patch gatewayclass`
w Kroku 3.

**kind** — nie ma cloud-providera, więc `LoadBalancer` zostałby `pending`. Przypinamy
poda Envoya do control-plane i otwieramy na nim `hostPort`:

```sh
kubectl apply -f envoyproxy-hostport.yaml
```

> Envoy jako nie-root nie zbinduje portów <1024, więc nasłuchuje na **porcie listenera
> +10000**: 80 → 10080, 443 → 10443. Stąd `hostPort: 80 → containerPort: 10080`.
> Przepływ: `host:80 → node:80 (kind.yaml) → hostPort → Envoy:10080`.
> Pod wyląduje na control-plane (jedyny node z `ingress-ready=true`); `toleration`
> w pliku pozwala mu tam usiąść mimo taintu.

---

## Krok 3 — Sanity check

```sh
kubectl apply -f gateway-http.yaml -f backends.yaml

# catch-all: bez hostnames -> łapie każdy Host header (też goły localhost)
kubectl apply -f - <<'EOF'
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: welcome
spec:
  parentRefs:
    - name: training-gateway
  rules:
    - backendRefs:
        - name: demo-app
          port: 80
EOF

# TYLKO kind: GatewayClass "eg" już istnieje, więc podpinamy pod nią EnvoyProxy z Kroku 2.
kubectl patch gatewayclass eg --type=merge -p '{"spec":{"parametersRef":{"group":"gateway.envoyproxy.io","kind":"EnvoyProxy","name":"workshop-hostport","namespace":"envoy-gateway-system"}}}'

kubectl wait --for=condition=Programmed gateway/training-gateway --timeout=120s

curl -s http://localhost/ | grep -o '<title>.*</title>'
# <title>Welcome to nginx!</title>
```

> `Programmed` długo `False`? kind → brak `patch gatewayclass`.
> Docker Desktop → `EXTERNAL-IP <pending>` oznacza zajęty `:80`/`:443` na hoście.

Widzisz HTML nginxa → ruch dociera do Envoya, HTTPRoute jest podpięty. `welcome`
zostaje; bardziej specyficzne route'y poniżej wygrywają z nim dla swoich domen
(most-specific-match).

---

## Przykład 1 — Routing po ścieżce (fanout)

```sh
kubectl apply -f fanout/httproute-path.yaml

curl http://demo.127-0-0-1.nip.io/         # -> nginx (demo-app)
curl http://demo.127-0-0-1.nip.io/echo     # -> echo-server, odbija request
```

## Przykład 2 — Routing po nazwie hosta (nip.io)

```sh
kubectl apply -f host/httproute-host.yaml

curl http://nginx.127-0-0-1.nip.io/        # -> nginx
curl http://echo.127-0-0-1.nip.io/         # -> echo-server
```

`<cokolwiek>.127-0-0-1.nip.io` rozwiązuje się na `127.0.0.1` — bez ruszania `/etc/hosts`.
Envoy dopasowuje regułę po nagłówku `Host`.

## Przykład 3 (bonus) — URLRewrite zamiast adnotacji

```sh
kubectl apply -f fanout/httproute-rewrite.yaml

curl http://demo.127-0-0-1.nip.io/legacy/v1   # echo pokaże, że backend dostał "/v1"
```

To, co w Ingress wymagało `nginx.ingress.kubernetes.io/rewrite-target`, tu jest
typowanym filterem `URLRewrite` w spec — przenośnym między implementacjami.

## Przykład 4 — TLS

Patrz **[`tls/README.md`](tls/README.md)**: self-signed (openssl) → cert-manager
`selfSigned` (lokalnie) → Let's Encrypt (produkcja).

### cert-manager bez Helma (do Przykładu 4B/4C)

```sh
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.21.0/cert-manager.yaml
kubectl wait --timeout=180s -n cert-manager \
  deployment/cert-manager deployment/cert-manager-webhook --for=condition=Available
```

Issuer `selfSigned` (4B) działa od razu. Let's Encrypt (4C) wymaga publicznego IP,
więc lokalnie zostajemy przy 4A/4B. Na klastrze w chmurze cert-manager potrzebuje
dodatkowo solvera Gateway (`gateway-shim`):

```sh
kubectl -n cert-manager patch deploy cert-manager --type=json \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--enable-gateway-api"}]'

kubectl -n cert-manager rollout status deploy/cert-manager
```

Bez tej flagi Challenge wisi w `pending` z `gateway api is not enabled`.

### 4C — Let's Encrypt na DigitalOcean (Cilium, prawdziwy zaufany cert)

Na DOKS nie ma Envoy Gateway — używamy wbudowanego Cilium (patrz sekcja DOKS w Kroku 1).
`gateway-http.yaml`/`gateway-https.yaml` są dla `eg`, więc tu Gateway definiujemy inline z
`gatewayClassName: cilium`. Nazywamy go `training-gateway`, żeby `tls/certmanager-letsencrypt.yaml`
(solver + HTTPRoute + Certificate) pasował bez zmian.

```sh
kubectl apply -f backends.yaml

# 1) Gateway (listener HTTP) — DO nada publiczny EXTERNAL-IP
kubectl apply -f - <<'EOF'
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata: { name: training-gateway, namespace: default }
spec:
  gatewayClassName: cilium
  listeners:
    - { name: http, protocol: HTTP, port: 80, allowedRoutes: { namespaces: { from: All } } }
EOF
kubectl wait --for=condition=Programmed gateway/training-gateway --timeout=180s
IP=$(kubectl get gateway training-gateway -o jsonpath='{.status.addresses[0].value}')

# 2) pre-flight HTTP-01 (404 z backendu = ścieżka drożna; refused/timeout = NIE wystawiaj certu)
curl -s -o /dev/null -w "%{http_code}\n" http://app.$IP.nip.io/.well-known/acme-challenge/probe

# 3) issuer prod + Certificate + HTTPRoute (placeholder <GATEWAY-IP> -> realny IP)
sed "s/<GATEWAY-IP>/$IP/g" tls/certmanager-letsencrypt.yaml | kubectl apply -f -
kubectl wait --for=condition=Ready certificate/app-tls --timeout=5m

# 4) dorzuć listener HTTPS (Cilium terminuje TLS Secretem app-tls)
kubectl apply -f - <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata: { name: training-gateway, namespace: default }
spec:
  gatewayClassName: cilium
  listeners:
    - { name: http, protocol: HTTP, port: 80, allowedRoutes: { namespaces: { from: All } } }
    - name: https
      protocol: HTTPS
      port: 443
      hostname: app.$IP.nip.io
      tls: { mode: Terminate, certificateRefs: [ { kind: Secret, name: app-tls } ] }
      allowedRoutes: { namespaces: { from: All } }
EOF

curl -sv https://app.$IP.nip.io/ 2>&1 | grep -iE 'issuer:|subject:'
# issuer: C=US; O=Let's Encrypt  -> zaufany łańcuch, curl BEZ -k
```

> Plik używa od razu `letsencrypt-prod` — zielona kłódka bez `-k`. Ceną jest limit LE:
> **5 nieudanych walidacji na godzinę na hostname**, dlatego pre-flight `curl` w kroku 2.

---

## Sprzątanie

```sh
kubectl delete -f host/ -f fanout/ -f backends.yaml --ignore-not-found
kubectl delete httproute welcome --ignore-not-found
kubectl delete -f gateway-http.yaml --ignore-not-found
# po Przykładzie 4 (TLS):
kubectl delete secret app-tls --ignore-not-found
kubectl delete -f tls/certmanager-selfsigned.yaml --ignore-not-found
# (opcjonalnie) Envoy Gateway / cert-manager:
# kubectl delete -f https://github.com/envoyproxy/gateway/releases/download/v1.8.2/install.yaml
```

Na **DOKS** (Przykład 4C, Cilium) — LoadBalancer DO kosztuje, więc po demie skasuj Gateway:

```sh
kubectl delete gateway training-gateway --ignore-not-found   # zwalnia LB DO
kubectl delete httproute app-public --ignore-not-found
kubectl delete certificate app-tls --ignore-not-found
kubectl delete clusterissuer letsencrypt-prod --ignore-not-found
kubectl delete secret app-tls --ignore-not-found
```

## Linki
- [Gateway API](https://gateway-api.sigs.k8s.io/)
- [Envoy Gateway](https://gateway.envoyproxy.io/)
- [cert-manager](https://cert-manager.io/docs/)
- [nip.io](https://nip.io/)
- [ingress2gateway — migracja Ingress → Gateway API](https://github.com/kubernetes-sigs/ingress2gateway)
