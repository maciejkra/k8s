## Taints

https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/

taint node

```sh
kubectl taint nodes ubuntu2 key=value:NoSchedule
kubectl create -f python-deployment.yml
kubectl describe pod -l app=python-taints
# remove comments
kubectl apply -f python-deployment.yml
kubectl describe pod -l app=python-taints

# untaint
kubectl taint nodes ubuntu2 key:NoSchedule-
```

evict pods
```sh
kubectl taint nodes ubuntu2 key=value1:NoExecute
kubectl get pods
kubectl taint nodes ubuntu2 key=value1:NoExecute-

```