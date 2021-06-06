```sh
kubectl create secret generic my-secret --from-file=./my-secrets --from-literal=user=maciek
kubectl get secret my-secret -o yaml
```
https://kubernetes.io/docs/concepts/configuration/secret/

https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
