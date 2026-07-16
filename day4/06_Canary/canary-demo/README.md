# Canary Deployments with Gateway API
## Overview
Weighted canary release na Gateway API (Envoy Gateway). Podział ruchu to pole `weight`
w `HTTPRoute` — nie adnotacja kontrolera. Wagi zmieniamy na żywo, bez restartu podów.

## Requirements
* Klaster Kubernetes
* Envoy Gateway + działający Gateway `training-gateway` — patrz `day3/07_gateway_api`
* `hey` (`brew install hey`) i `jq`

## Getting Started

### Canary Test Scenario

##### Deploy both releases
Stable 1.0.0 (`demo-prod`) i canary 1.0.1 (`demo-canary`):
```bash
$ make step-1
$ make step-2
```
Oba Service'y muszą istnieć, zanim powstanie `HTTPRoute` — Gateway API rozwiązuje każdy
`backendRef` niezależnie od jego wagi.

##### Route the traffic
```bash
$ make deploy-route
$ kubectl get httproute canary-demo -o jsonpath='{.status.parents[0].conditions[?(@.type=="ResolvedRefs")].status}'
```
Musi zwrócić `True`. `deploy-route` tworzy `HTTPRoute` (100/0 — canary jest wdrożony,
ale nie dostaje ruchu) plus dwa `ReferenceGrant`. Grant jest potrzebny, bo `HTTPRoute`
żyje w `default`, a Service'y w `demo-prod`/`demo-canary` — Gateway API wymaga jawnej
zgody na cross-namespace, czego Ingress nie potrzebował.

##### Run tests
```bash
$ hey -n 1000 -c 100 "http://canary-demo.127-0-0-1.nip.io/version"
$ curl -s "http://canary-demo.127-0-0-1.nip.io/metrics" | jq '.calls'
```
Przy 100/0 cały ruch idzie do `demo-prod` — 1000 odpowiedzi `[200]`.

> Nie używaj `ab` — wysyła HTTP/1.0, na co Envoy odpowiada `426 Upgrade Required`.
> Pierwszy przebieg na zimnych podach może dać kilka `504`; powtórz.

##### Shift traffic to canary
Ten sam obiekt, zmienione wagi — bez `kubectl apply` na deploymentach:
```bash
$ kubectl patch httproute canary-demo --type=json \
    -p='[{"op":"replace","path":"/spec/rules/0/backendRefs/0/weight","value":80},
         {"op":"replace","path":"/spec/rules/0/backendRefs/1/weight","value":20}]'
```

##### Verify the weight split
Zeruj liczniki na obu podach (`/reset` przez gateway trafiłby tylko w jeden) i puść ruch:
```bash
$ kubectl -n demo-prod   port-forward deployment/demo-prod   8080:8080 &
$ kubectl -n demo-canary port-forward deployment/demo-canary 8081:8080 &
$ curl -s http://localhost:8080/reset && curl -s http://localhost:8081/reset

$ hey -n 1000 -c 100 "http://canary-demo.127-0-0-1.nip.io/version"

$ curl -s http://localhost:8080/metrics | jq '.calls'   # ~800
$ curl -s http://localhost:8081/metrics | jq '.calls'   # ~200
```
Rozkład jest losowy, więc ~800/200, nie dokładnie. Sprawdź `kubectl -n demo-prod get pods`
— `RESTARTS` dalej `0`: przesunięcie ruchu nie dotknęło podów.

Kolejne etapy: 50/50, 20/80, 0/100 — tym samym patchem.

### Delete
```bash
$ make clean-up
```
`clean-up` kasuje cały `./deploy/`, łącznie z `httproute.yaml` i `ReferenceGrant`ami.
