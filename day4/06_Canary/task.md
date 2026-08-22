# Zadanie — Canary (weighted routing 70:30)

Wymaga Gateway API z D3/07 (`training-gateway`, `Programmed=True`) oraz backendów
z `day3/07_gateway_api/backends.yaml` (`demo-app` = nginx, `echo-app` = echo-server).

Cel: rozłożyć ruch przez jeden `HTTPRoute` z `backendRefs[].weight` — **70% na demo-app, 30% na echo-app**.

> Zadanie jest niezależne od demo z `canary-demo/` — inna nazwa HTTPRoute (`canary-task`)
> i inny hostname (`canary.` vs `canary-demo.`), więc oba mogą stać w klastrze naraz.

## Część 1 — dwa backendy

```sh
kubectl apply -f ../../day3/07_gateway_api/backends.yaml
kubectl get svc demo-app echo-app
```

Oba Service'y muszą istnieć, **zanim** powstanie `HTTPRoute` — Gateway API rozwiązuje
każdy `backendRef` niezależnie od jego wagi (także tej równej 0).

## Część 2 — weighted HTTPRoute 70/30

Napisz `HTTPRoute` na `training-gateway` z dwoma `backendRefs`: `demo-app:80` (weight 70)
i `echo-app:80` (weight 30). Gotowiec: `solution/httproute-canary.yaml`.

```sh
kubectl apply -f solution/httproute-canary.yaml
kubectl describe httproute canary-task   # Accepted=True, ResolvedRefs=True
```

## Część 3 — test rozkładu

```sh
for i in $(seq 1 100); do
  curl -s canary.127-0-0-1.nip.io/ | grep -qi nginx && echo nginx || echo echo
done | sort | uniq -c
# ~70 nginx, ~30 echo (±5%)
```

## Część 4 — przesuwanie ruchu

Zmień weighty (np. 50/50, potem 0/100), re-apply i ponów pomiar — zmiana jest natychmiastowa,
bez restartu Podów:
```sh
kubectl patch httproute canary-task --type=json -p='[
  {"op":"replace","path":"/spec/rules/0/backendRefs/0/weight","value":50},
  {"op":"replace","path":"/spec/rules/0/backendRefs/1/weight","value":50}
]'
```

Sprawdź `kubectl get pods` — `RESTARTS` dalej `0`: przesunięcie ruchu nie dotknęło Podów.

W produkcji po każdym kroku: pauza na monitoring (error rate, latency p99); jeśli SLO spada
→ rollback (przywróć weight).

## Sprzątanie

```sh
kubectl delete -f solution/httproute-canary.yaml --ignore-not-found
```
