# Manual expose

```sh
kubectl expose pod myapp-pod --type=NodePort --port=80
```


```sh
kubectl get service
```
Go to `<IP of worker node>:<exposed port>`

# Expose using declarative approach

```sh
kubectl apply -f service.yaml
kubectl exec -ti myapp-pod -- curl my-app-service
kubectl exec -ti myapp-pod -- curl my-app-service.default.svc.cluster.local

kubectl exec -ti myapp-pod -- cat /etc/resolv.conf
```
