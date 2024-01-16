# Docs
ref: https://kubernetes.io/docs/reference/access-authn-authz/authentication/

# Creation
```sh
kubectl apply -f sa.pod-reader.yaml
kubectl apply -f cluster-role.yaml
kubectl apply -f rbac.yaml
kubectl apply -f pod.yml
```
# Get the ServiceAccount token from within the Pod's container
```sh
TOKEN=$(cat /run/secrets/kubernetes.io/serviceaccount/token)
curl -H "Authorization: Bearer $TOKEN" https://kubernetes/api/v1/namespaces/default/pods/ --insecure
```

Run pod with `kubectl`
```sh
kubectl apply -f pod-kctl.yaml
kubectl logs pod-reader
```