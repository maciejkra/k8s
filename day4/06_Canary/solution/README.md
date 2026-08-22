# Solution — 06_Canary

## Architektura

```
       Client
         │  curl canary.127-0-0-1.nip.io
         ▼
   [Envoy Gateway]  (D3/07 training-gateway)
         │
         ▼
   [HTTPRoute canary-task]  ← weighted routing 70/30
         ├──70%──→ Service demo-app ──→ nginx
         └──30%──→ Service echo-app ──→ echo-server
```

## Pliki
- `httproute-canary.yaml` — HTTPRoute z `backendRefs[].weight` 70 (demo-app) / 30 (echo-app)
- oba backendy pochodzą z `day3/07_gateway_api/backends.yaml`

Weighted HTTPRoute vs stary wzorzec (ratio replik na wspólnym Service):

| | Stare (ratio replik) | Weighted HTTPRoute |
|---|---|---|
| Sterowanie ratio | `replicas` (1% = 100 Podów) | `weight` (dowolna %) |
| Koszt zmiany | skalowanie Podów | update manifestu, Envoy ~1s, bez restartu |
| Osobna konfiguracja backendów | trudna (wspólny Service) | łatwa (osobne Service) |
| Routing po header/cookie | niemożliwy | `matches.headers` w regule |

## Apply

```sh
# Gateway training-gateway z D3/07 musi istnieć i być Programmed
kubectl apply -f ../../../day3/07_gateway_api/backends.yaml
kubectl apply -f httproute-canary.yaml
sleep 5   # Envoy program config
```

## Walidacja

```sh
for i in $(seq 1 100); do
  curl -s canary.127-0-0-1.nip.io/ | grep -qi nginx && echo nginx || echo echo
done | sort | uniq -c
# ~70 nginx, ~30 echo (±5%)
```

## Przesuwanie ruchu

```sh
# 50/50
kubectl patch httproute canary-task --type=json -p='[
  {"op":"replace","path":"/spec/rules/0/backendRefs/0/weight","value":50},
  {"op":"replace","path":"/spec/rules/0/backendRefs/1/weight","value":50}
]'

# 100% canary
kubectl patch httproute canary-task --type=json -p='[
  {"op":"replace","path":"/spec/rules/0/backendRefs/0/weight","value":0},
  {"op":"replace","path":"/spec/rules/0/backendRefs/1/weight","value":100}
]'
```

W produkcji **Argo Rollouts** / **Flagger** robią to automatycznie — monitorują SLO
(error rate, latency) między krokami i rollują wstecz przy przekroczeniu progu.

## Header-based routing (preview)

Tylko ruch z nagłówkiem `x-canary-tester: true` → echo-app, reszta → demo-app:

```yaml
rules:
  - matches:
      - headers:
          - name: x-canary-tester
            value: "true"
    backendRefs:
      - name: echo-app
        port: 80
  - matches:
      - path: { type: PathPrefix, value: / }
    backendRefs:
      - name: demo-app
        port: 80
```

```sh
curl -H "x-canary-tester: true" canary.127-0-0-1.nip.io/   # zawsze echo-server
curl canary.127-0-0-1.nip.io/                              # zawsze nginx
```
