```sh
kubectl get pod
kubectl apply -f replica-set.yaml
kubectl get pod -o wide
```
# change pod name
```sh
kubectl apply -f pod.yaml
kubectl get pod -o wide
```

# delete pod
```sh
kubectl delete pod myapp-pod
kubectl get pod -o wide
```
# scale replica
```sh
kubectl scale rs replicate-my-app --replicas=3
kubectl get pod -o wide
```
# delete replica set
```sh
kubectl delete rs replicate-my-app
kubectl get pod -o wide
```
# delete & keep pods
```sh
kubectl apply -f replica-set.yaml
kubectl get rs
kubectl describe rs replicate-my-app
kubectl delete rs replicate-my-app --cascade=false
kubectl get rs
kubectl get pod -o wide
```
