Do this first!

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

Get pods for my project

```sh
kubectl get pods -l app=myapp
```

Get specific pod name

```sh
kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}'
```

Gell all logs

```sh
kubectl logs -l app=myapp
```

Some hardcore stuff

```sh
kubectl delete svc --all
```

List all Persistent Volumes sorted by their name

```sh
kubectl get pv | grep -v NAME | sort -k 2 -rh
```

Save the manifest of a running pod
```sh
kubectl get pod <name> -o yaml > pod.yml

```

```sh
kubectl get all
```
