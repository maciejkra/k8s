# Create deployment

```sh
kubectl apply -f deployment.yaml
kubectl get all
kubectl scale deployment/nginx-deployment --replicas=0
kubectl get all
```

# Use env variable
add `env` list

```sh
kubectl rollout history deployments/nginx-deployment
kubectl apply -f deployment.yaml

kubectl rollout status deployment/nginx-deployment
kubectl rollout history deployment/nginx-deployment --revision=1
kubectl rollout history deployment/nginx-deployment --revision=2
kubectl annotate deployment/nginx-deployment kubernetes.io/change-cause="env updated"
kubectl rollout history deployments/nginx-deployment
```

# Exec container and check env exists:

```sh
kubectl get pods
kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}'
kubectl exec -ti $(kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}') -- env | grep TEST_ENV
```

# Rollback to previous version

```sh
kubectl rollout undo deployment/nginx-deployment
kubectl annotate deployment/nginx-deployment kubernetes.io/change-cause="env removed"
kubectl rollout history deployments/nginx-deployment

kubectl exec -ti $(kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}') -- env | grep TEST_ENV

kubectl rollout undo deployment/nginx-deployment --to-revision=2
kubectl exec -ti $(kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}') -- env | grep TEST_ENV
```

# Scale deployment 
```sh
kubectl describe svc my-app-service
kubectl scale deployment nginx-deployment --replicas=3
kubectl describe svc my-app-service
```
 - check endpoints


# Debug information:
```sh
kubectl logs -l app=myapp
kubectl exec -ti $(kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}') -- cat /etc/resolv.conf
kubectl exec -ti $(kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}') -- curl my-app-service
kubectl logs -l app=myapp
kubectl get rs
```
