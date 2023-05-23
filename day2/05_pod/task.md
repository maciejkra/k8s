1. Create pod with python application from `krajewskim/python-api:new` image
2. Use port forward (5002) and check `/healthz` endpoint
3. Check logs

```sh
kubectl logs <pod-name>
```

4. Describe pod

```sh
kubectl describe pod <pod-name>
```
