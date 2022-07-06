Do this first!

# Create a K8s kluster with kind
Please change `hostPath` in `kind.yaml` first.

for windows change `hostPath` to `/c/path/to/file`

```sh
kind create cluster --config ./kind.yaml --name workshop
```


```sh
kubectl config current-context
kubectl config get-contexts
```

info:
```sh
kubectl cluster-info
```

Really verbose

```sh
kubectl get pods -v=9
```
