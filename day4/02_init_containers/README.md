https://kubernetes.io/docs/concepts/workloads/pods/init-containers/


```sh
kubectl create -f initc.pod.yaml
kubectl get pods myapp-pod
kubectl create -f redis.yaml
kubectl logs myapp-pod init-myservice
kubectl get pods myapp-pod
```