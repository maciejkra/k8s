## Install kube-prometheus-stack

```sh
helm upgrade --install --wait --timeout 15m \
  --namespace monitoring --create-namespace \
  --repo https://prometheus-community.github.io/helm-charts \
  kube-prometheus-stack kube-prometheus-stack
```

Retrieve the password to log into Grafana (user `admin`):
```sh
kubectl get secret -n monitoring kube-prometheus-stack-grafana \
  -o jsonpath='{.data.admin-password}' | base64 --decode ; echo
```

Access the Grafana UI:
```sh
kubectl port-forward -n monitoring service/kube-prometheus-stack-grafana 3000:80
```

## Install Loki + Alloy via Helm

```sh
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# backend
helm upgrade --install loki grafana/loki \
  --namespace loki --create-namespace -f loki-values.yaml --timeout 10m

# kolektor logów
helm upgrade --install alloy grafana/alloy \
  --namespace alloy --create-namespace -f alloy-values.yaml
```

Dodaj w Grafanie data source typu **Loki** pod adresem:

```
http://loki-gateway.loki.svc.cluster.local/
```

Sprawdź w Grafanie → Explore → Loki, np. `{namespace="kube-system"}`.

## Linki
- [Loki Helm chart](https://grafana.com/docs/loki/latest/setup/install/helm/)
- [Grafana Alloy](https://grafana.com/docs/alloy/latest/)
