https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

# Create crd

```sh
kubectl apply -f bash-operator/kubernetes
kubectl get CustomResourceDefinition
kubectl get CustomResourceDefinition podcreators.bash-operators.maciej
kubectl get podcreators
```

```sh
kubectl apply -f bash-operator/example
kubectl get podcreators
kubectl logs -l app=pod-creator
kubectl get pod
kubectl get po | grep maciej
```
