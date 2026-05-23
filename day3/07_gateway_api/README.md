# 07 — Gateway API (Envoy Gateway)

Następca **Ingress**. Ingress jest dziś legacy — routing po hoście/ścieżce, a wszystko
inne (rewrite, TLS, nagłówki) przez adnotacje specyficzne dla kontrolera ("annotation
hell"). Gateway API (GA od K8s 1.29) robi to deklaratywnie, w typowanych obiektach:

| Obiekt         | Co opisuje                                   | Odpowiednik w Ingress |
|----------------|----------------------------------------------|-----------------------|
| `GatewayClass` | KTÓRA implementacja (Envoy, NGINX, Cilium…)  | `IngressClass`        |
| `Gateway`      | instancja LB: porty i listenery (80/443)     | część `Ingress`       |
| `HTTPRoute`    | reguły routingu (host, path, filtry)         | `rules:` w `Ingress`  |

W tym ćwiczeniu używamy **Envoy Gateway** i dwóch samodzielnych backendów (`nginx` +
`echo-server` z `backends.yaml`) — bez zależności od aplikacji z innych dni.

---

## Wymagania

Jeden z dwóch klastrów lokalnych:
- **kind** — klaster `workshop` z `day2/04_k8s/kind.yaml` (control-plane ma label
  `ingress-ready=true` i mapowanie portów 80/443 na host), **albo**
- **Docker Desktop** — z włączonym Kubernetesem (Settings → Kubernetes → Enable).

> **Uwaga o portach 80/443:** muszą być wolne na hoście. Jeśli coś już je zajmuje
> (`sudo lsof -nP -iTCP:80 -sTCP:LISTEN`), zatrzymaj to — inaczej ruch z `localhost`
> nie dojdzie do klastra.

---

## Krok 1 — Instalacja Envoy Gateway (bez Helma)

Helm poznajemy dopiero w `day5/05_helm`. Tu instalujemy zwykłym `kubectl apply`
z gotowego manifestu (analogicznie do `deploy.yaml` ingress-nginx, którego używaliśmy
wcześniej):

```sh
kubectl apply --server-side -f https://github.com/envoyproxy/gateway/releases/download/v1.3.2/install.yaml

kubectl wait --timeout=180s -n envoy-gateway-system \
  deployment/envoy-gateway --for=condition=Available
```

`install.yaml` zawiera CRD-y Gateway API + samego Envoy Gateway. **Nie** tworzy
`GatewayClass` — robi to za nas `gateway-http.yaml` w Kroku 3.

---

## Krok 2 — Ekspozycja na hoście

Cel: dostać się do Envoya z hosta. Sposób zależy od klastra.

### Docker Desktop — nic nie trzeba

Docker Desktop ma wbudowany LoadBalancer: domyślny Service `LoadBalancer` data-plane'u
Envoya dostaje `EXTERNAL-IP: localhost` i jest wystawiony na `localhost:80` / `:443`.
Po Kroku 3 `curl http://localhost/` zadziała wprost. Pomiń sekcję kind poniżej oraz
`kubectl patch gatewayclass` w Kroku 3.

> **Warunek:** porty `:80`/`:443` na hoście muszą być wolne. Jeśli trzyma je inny
> kontener/aplikacja (np. lokalny Traefik/NGINX), LoadBalancer zostanie `EXTERNAL-IP
> <pending>` i `curl http://localhost/` trafi w tamtą aplikację. Zwolnij porty
> (`sudo lsof -nP -iTCP:80 -sTCP:LISTEN`, zatrzymaj proces) i odśwież Gateway.

### kind (`workshop`) — przypnij data-plane do control-plane

kind nie ma cloud-providera, więc `LoadBalancer` zostałby `pending`. Przypinamy poda
Envoya do node'a z portami 80/443 i otwieramy na nim `hostPort` (to samo, co robiliśmy
nodeSelector-patchem dla ingress-nginx — tu w obiekcie `EnvoyProxy`). Tu aplikujemy
sam obiekt `EnvoyProxy`; podpięcie go pod GatewayClass `eg` jest w Kroku 3 (bo `eg`
powstaje dopiero tam):

```sh
kubectl apply -f envoyproxy-hostport.yaml
```

> Detal, który łatwo przeoczyć: Envoy (jako nie-root) nie zbinduje portów <1024,
> więc nasłuchuje na **porcie listenera +10000** — listener 80 → kontener 10080,
> 443 → 10443. Dlatego `envoyproxy-hostport.yaml` mapuje `hostPort: 80 → containerPort: 10080`.
> Przepływ: `host:80 → node:80 (kind.yaml) → hostPort → Envoy:10080`.
> Pod Envoya wyląduje na control-plane (jedyny node z `ingress-ready=true`); na
> Twoim 4-nodowym `workshop` `toleration` w pliku pozwala mu tam usiąść mimo taintu.

---

## Krok 3 — Sanity check (zanim wejdziemy w nip.io)

Stwórz GatewayClass + Gateway + backendy + prosty catch-all route i sprawdź plumbing:

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

# TYLKO kind: teraz GatewayClass "eg" istnieje — podepnij pod nią EnvoyProxy z Kroku 2.
# (Docker Desktop: pomiń tę komendę.) Po patchu data-plane się przeładuje.
kubectl patch gatewayclass eg --type=merge -p '{"spec":{"parametersRef":{"group":"gateway.envoyproxy.io","kind":"EnvoyProxy","name":"workshop-hostport","namespace":"envoy-gateway-system"}}}'

kubectl wait --for=condition=Programmed gateway/training-gateway --timeout=120s

curl -s http://localhost/ | head -3
# <!DOCTYPE html> / <html> / <title>Welcome to nginx!</title>
```

> **Jeśli `Programmed` długo jest `False`:**
> - kind → najczęściej brak `patch gatewayclass` (data-plane nie wstał na control-plane);
> - Docker Desktop → `AddressNotAssigned`/`EXTERNAL-IP <pending>` oznacza zajęty `:80`/`:443`
>   na hoście (inny kontener) — zwolnij porty.

Widzisz HTML nginxa → ruch z hosta dociera do Envoya, GatewayClass reconciluje,
HTTPRoute jest podpięty. `welcome` zostaje na czas ćwiczenia; bardziej specyficzne
route'y poniżej wygrywają z nim dla swoich domen (Gateway API: most-specific-match).

Na obu klastrach adresy w przykładach niżej są wprost: `curl http://<host>/` (port 80).

---

## Przykład 1 — Routing po ścieżce (fanout)

```sh
kubectl apply -f fanout/httproute-path.yaml

curl http://demo.127-0-0-1.nip.io/         # -> nginx (demo-app)
curl http://demo.127-0-0-1.nip.io/echo     # -> echo-server (echo-app), odbija request
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
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.2/cert-manager.yaml
kubectl wait --timeout=180s -n cert-manager \
  deployment/cert-manager deployment/cert-manager-webhook --for=condition=Available
```

> Issuer `selfSigned` (4B) działa od razu. Dla Let's Encrypt + Gateway API (4C)
> cert-manager musi mieć włączony solver Gateway (`gateway-shim`) — w instalacji bez
> Helma dodaje się to flagą kontrolera `--enable-gateway-api`
> (`kubectl -n cert-manager set args ...` / edycja Deploymentu). Lokalnie i tak
> nieosiągalne (brak publicznego IP), więc na kursie zostajemy przy 4A/4B.

---

## Sprzątanie

```sh
kubectl delete -f host/ -f fanout/ -f backends.yaml --ignore-not-found
kubectl delete httproute welcome --ignore-not-found
kubectl delete -f gateway-http.yaml --ignore-not-found
# (opcjonalnie) Envoy Gateway / cert-manager:
# kubectl delete -f https://github.com/envoyproxy/gateway/releases/download/v1.3.2/install.yaml
```

## Linki
- [Gateway API](https://gateway-api.sigs.k8s.io/)
- [Envoy Gateway](https://gateway.envoyproxy.io/)
- [cert-manager](https://cert-manager.io/docs/)
- [nip.io](https://nip.io/)
- [ingress2gateway — migracja Ingress → Gateway API](https://github.com/kubernetes-sigs/ingress2gateway)
