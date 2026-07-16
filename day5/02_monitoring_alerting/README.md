## Install Loki via Helm
Add Loki’s Helm Chart repository:

```
helm repo add grafana https://grafana.github.io/helm-charts
```

Run the following command to update the repository:

```
helm repo update
```

Deploy the Loki stack:
```
helm upgrade --install loki grafana/loki-stack  --set grafana.enabled=true,prometheus.enabled=true,prometheus.alertmanager.persistentVolume.enabled=false,prometheus.server.persistentVolume.enabled=false --namespace=loki --create-namespace
```
> `loki-stack` jest oznaczony przez Grafana Labs jako deprecated (wciąż działa, ale
> instaluje Loki 2.9). Następca to osobne charty `grafana/loki` + `grafana/alloy`.
This will install Loki, Grafana and Promtail into your Kubernetes cluster.

Retrieve the password to log into Grafana:
```
kubectl get secret loki-grafana --namespace=loki -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```
The generated admin password will look like this one -> `<40-znakowy losowy ciąg>`

Finally, execute the command below to access the Grafana UI.
```
kubectl port-forward --namespace loki service/loki-grafana 3000:80
```

https://grafana.com/docs/loki/latest/installation/helm/?pg=get&plcmt=selfmanaged-box2-cta2