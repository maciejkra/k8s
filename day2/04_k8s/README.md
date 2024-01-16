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

### Install autocomplete for kubectl
* [For Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#enable-shell-autocompletion)
* [For Windows](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#enable-shell-autocompletion)
* [For Mac](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)

