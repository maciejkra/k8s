```
kubectl apply -f google-service.yaml
kubectl exec -ti myapp-pod -- curl google-service
```

kubectl get svc
kubectl get endpoints


# Default ENV exposed example

- REDIS_MASTER_SERVICE_HOST=10.0.0.11
- REDIS_MASTER_SERVICE_PORT=6379
- REDIS_MASTER_PORT=tcp://10.0.0.11:6379
- REDIS_MASTER_PORT_6379_TCP=tcp://10.0.0.11:6379
- REDIS_MASTER_PORT_6379_TCP_PROTO=tcp
- REDIS_MASTER_PORT_6379_TCP_PORT=6379
- REDIS_MASTER_PORT_6379_TCP_ADDR=10.0.0.11
