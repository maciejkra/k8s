1. Create pod with python flask application
2. Port forward and check /healthz endpoint
3. Check logs

```sh
kubectl logs <pod-name>
```

4. Describe pod

```sh
kubectl describe pod <pod-name>
```