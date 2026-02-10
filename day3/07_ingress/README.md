```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.3/deploy/static/provider/cloud/deploy.yaml
```

for KIND please use
```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

kubectl -n ingress-nginx patch deploy ingress-nginx-controller \
  --type='json' \
  -p='[
    {"op":"add","path":"/spec/template/spec/nodeSelector","value":{"kubernetes.io/hostname":"workshop-control-plane"}}
  ]'

```

# Worth Reading
https://kubernetes.io/docs/concepts/services-networking/ingress/

https://kubernetes.github.io/ingress-nginx/

https://cert-manager.io/docs/
