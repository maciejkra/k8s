```sh
kubectl get pod
kubectl apply -f replica-set.yaml
kubectl get all
```
# change pod name
```sh
kubectl apply -f pod.yaml
kubectl get pod
```

# delete pod
```sh
kubectl delete pod myapp-pod
kubectl get pod
```
# scale replica
```sh
kubectl scale rs replicate-my-app --replicas=3
kubectl get all
```
# delete replica set
```sh
kubectl delete rs replicate-my-app
kubectl get all
```
# delete & keep pods
```sh
kubectl apply -f replica-set.yaml
kubectl get rs
kubectl describe rs replicate-my-app
kubectl delete rs replicate-my-app --cascade=false
kubectl get rs
kubectl get pod
```
