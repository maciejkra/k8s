## Limit by default

https://kubernetes.io/docs/concepts/policy/limit-range/

```sh
kubectl create -f limitrange.yaml
kubectl describe limitrange mem-limit-range
```

```sh
kubectl create ns test-1
kubectl create -f ns-quota.yaml
kubectl create -f deployment.yaml -n test-1
kubectl scale deployment -n test-1 nginx-readiness --replicas=3
kubectl -n test-1 describe deploy nginx-readines
kubectl -n test-1 describe rs $(kubectl -n test-1 get rs -o jsonpath='{.items[0].metadata.name}')
```

## Resource quotas

https://kubernetes.io/docs/concepts/policy/resource-quotas/