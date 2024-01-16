# TOKEN Auth


```sh
kubectl create ns maciek
```

Create SA
```sh
kubectl apply -f sa.yaml
```

Get the token
```sh
TOKEN=$(kubectl get -n maciek secret maciek-secret -o jsonpath='{.data.token}'|base64 --decode)

kubectl config set-credentials maciek --token=$TOKEN
kubectl config set-context maciek-context --cluster=docker-desktop --namespace=default --user=maciek
kubectl get pods
```

Give permissions
```sh
kubectl apply -f rbac.yaml
kubectl get pods
```

# RBAC

* [RBAC description](https://kubernetes.io/docs/reference/access-authn-authz/authorization/#determine-the-request-verb)
* [RBAC good practisces](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)


