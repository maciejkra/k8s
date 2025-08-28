https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/

create admin-user/rbac

```sh
kubectl apply -f admin-user.yaml
kubectl apply -f rbac-admin.yaml
```

find admin user:
```sh
kubectl -n kubernetes-dashboard get secret
kubectl -n kubernetes-dashboard describe secret admin-user-secret
```

or
```sh
kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret  -o jsonpath='{.items[0].metadata.name}')
```

Access dashboard

```sh
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443

```
