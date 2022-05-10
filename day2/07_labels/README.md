# Labels
Guidlines: https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/

```yml
tier: frontend
release: stable
tenant: tenantA
```

kubectl

```sh
kubectl get pods -A --show-labels
kubectl get pods -l environment=production,tier=frontend
kubectl get pods -A -l 'tier in(control-plane)'
kubectl get pods -A -l 'tier in(control-plane),component notin(kube-scheduler)'

kubectl label pod/myapp-pod test-label=my-label
kubectl get pods -l test-label=my-label
kubectl get pods -l 'test-label in (my-label)'
```

# Resources for set based selectors
- Job
- Deployment
- ReplicaSet
- DaemonSet
- StatefullSet

```yml
selector:
  matchLabels:
    component: redis
  matchExpressions:
    - {key: tier, operator: In, values: [cache]}
    - {key: environment, operator: NotIn, values: [dev]}
```