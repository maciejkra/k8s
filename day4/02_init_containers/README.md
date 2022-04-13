https://kubernetes.io/docs/concepts/workloads/pods/init-containers/


```sh
kubectl apply -f initc.pod.yaml
kubectl get pods myapp-pod
kubectl apply -f redis.yaml
kubectl logs myapp-pod init-myservice
kubectl get pods myapp-pod
```