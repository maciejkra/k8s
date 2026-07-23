# Gateway API + Let's Encrypt na DigitalOcean (DOKS)

Przykład 4C (prawdziwy, zaufany certyfikat) wymaga publicznego IP, więc nie da się go
zrobić na kind. Ten plik to ścieżka na DOKS — plus wyjaśnienie, dlaczego **Krok 1
z `../README.md` tam nie przechodzi**.

## Dlaczego instrukcja z Kroku 1 pada na DOKS

DOKS ma wbudowany Cilium z obsługą Gateway API, więc CRD-y Gateway API są **własnością
control-plane'u DigitalOceana**, nie Twoją:

```sh
kubectl get crd gateways.gateway.networking.k8s.io -o jsonpath='{.metadata.labels}{"\n"}{.metadata.annotations}{"\n"}'
# doks.digitalocean.com/managed:true, c3.doks.digitalocean.com/component:cilium
# gateway.networking.k8s.io/bundle-version:v1.2.1
```

Zarządza nimi field manager `c3` przez server-side apply i **pinuje je na Gateway API v1.2.1**.
`install.yaml` Envoy Gateway v1.8.2 niesie własne CRD-y w wersji v1.5.1, więc SSA odmawia
oddania pól:

```
Apply failed with 4 conflicts: conflicts with "c3":
- .metadata.annotations.gateway.networking.k8s.io/bundle-version
- .spec.versions
```

To nie jest błąd do obejścia `--force-conflicts` — nadpisane CRD-y kontroler DO może cofnąć
w dowolnym momencie (także w środku szkolenia) i rozjechać własną `GatewayClass cilium`.
Zamiast tego **dobieramy wersję Envoy Gateway do Gateway API, które DOKS pinuje**.

| Gateway API u dostawcy | Pasujący Envoy Gateway |
|------------------------|------------------------|
| v1.2.1 (DOKS dziś)     | **v1.3.x**             |
| v1.5.x                 | v1.8.x                 |

Sprawdź, co pinuje Twój klaster, zanim wybierzesz wersję — powyższe może się zmienić:

```sh
kubectl get crd gateways.gateway.networking.k8s.io \
  -o jsonpath='{.metadata.annotations.gateway\.networking\.k8s\.io/bundle-version}{"\n"}'
```

## Instalacja Envoy Gateway

Helmem, bo tylko on pominie CRD-y Gateway API należące do DO, a doinstaluje własne
CRD-y `gateway.envoyproxy.io` (Helm przy `install` tworzy CRD-y, a istniejące pomija):

```sh
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.3.2 \
  -n envoy-gateway-system --create-namespace

kubectl wait --timeout=180s -n envoy-gateway-system \
  deployment/envoy-gateway --for=condition=Available
```

**Zweryfikuj CRD-y — to najczęstszy punkt awarii.** Ma być 8:

```sh
kubectl get crd -o name | grep -c 'gateway.envoyproxy.io'
```

Jeśli jest 0 (np. ktoś użył `--skip-crds`), doinstaluj je ręcznie:

```sh
helm pull oci://docker.io/envoyproxy/gateway-helm --version v1.3.2 --untar
kubectl apply --server-side -f gateway-helm/crds/generated/
kubectl rollout restart deploy/envoy-gateway -n envoy-gateway-system
```

> `--server-side` jest tu **konieczne**. CRD `envoyproxies` ma ponad 256 kB i zwykły
> `kubectl apply` odbija go z `metadata.annotations: Too long: may not be more than
> 262144 bytes` — bo client-side apply zapisuje całość w adnotacji
> `last-applied-configuration`. SSA jej nie używa.

Kontroler bez CRD-ów startuje, ale jest bezużyteczny — w logach widać wtedy:

```sh
kubectl logs -n envoy-gateway-system deploy/envoy-gateway | grep 'CRD not found'
# EnvoyProxy CRD not found, skipping EnvoyProxy watch   <- tak wygląda awaria
```

Zostaną `UDPRoute`, `TCPRoute`, `ServiceImport`, `BackendTLSPolicy` — tych DOKS nie
dostarcza i do HTTP/HTTPS nie są potrzebne.

## Gateway i publiczny IP

Na DOKS **pomijamy** `envoyproxy-hostport.yaml` oraz `kubectl patch gatewayclass` z Kroku 2/3
— to obejścia braku load balancera w kind. Tutaj DO nada prawdziwy IP:

```sh
kubectl apply -f ../gateway-http.yaml -f ../backends.yaml

kubectl wait --for=condition=Accepted gatewayclass/eg --timeout=90s
kubectl wait --for=condition=Programmed gateway/training-gateway --timeout=180s

IP=$(kubectl get gateway training-gateway -o jsonpath='{.status.addresses[0].value}')
echo "$IP"
```

> Ten `patch gatewayclass` na DOKS jest wręcz szkodliwy: wskazuje `parametersRef` na zasób
> `EnvoyProxy`, którego może nie być, i wtedy `GatewayClass` zostaje w `Accepted=Unknown`
> → Gateway nigdy nie zostanie zaprogramowany, a objaw (`no accepted gatewayclass` w logach)
> nie wskazuje na przyczynę.

## Certyfikat

cert-manager jak w `../README.md`, z włączonym `--enable-gateway-api`. Potem podstaw IP
i aplikuj — plik `certmanager-letsencrypt.yaml` ma placeholder `<GATEWAY-IP>`:

```sh
sed "s/<GATEWAY-IP>/$IP/g" certmanager-letsencrypt.yaml | kubectl apply -f -
```

**Zanim ruszysz na prod, sprawdź drożność ścieżki HTTP-01.** Ten jeden `curl` chroni przed
limitem 5 nieudanych walidacji na godzinę:

```sh
curl -s -o /dev/null -w "%{http_code}\n" http://app.$IP.nip.io/.well-known/acme-challenge/probe
# 404 = dobrze (odpowiada backend, ruch przechodzi)
# connection refused / timeout = Gateway nie działa, NIE wystawiaj jeszcze certyfikatu
```

Czekaj na certyfikat i podnieś listener HTTPS:

```sh
kubectl wait --for=condition=Ready certificate/app-tls --timeout=5m
kubectl apply -f ../gateway-https.yaml

curl -sv https://app.$IP.nip.io/ 2>&1 | grep -iE 'issuer:|subject:'
# issuer: C=US; O=Let's Encrypt  -> zaufany cert, curl BEZ -k
```

Certyfikat ze stagingu wystawi `Pretend Pear X1` i `curl` bez `-k` go odrzuci — to poprawne
zachowanie, nie błąd. Zaufany łańcuch dostaniesz dopiero po przełączeniu `issuerRef`
na `letsencrypt-prod`.

## Sprzątanie

Load balancer DO kosztuje, więc po demie:

```sh
kubectl delete -f ../gateway-http.yaml --ignore-not-found   # kasuje Gateway -> zwalnia LB
kubectl delete httproute app-public --ignore-not-found
kubectl delete certificate app-tls --ignore-not-found
kubectl delete clusterissuer letsencrypt-staging letsencrypt-prod --ignore-not-found
kubectl delete secret app-tls --ignore-not-found
```
