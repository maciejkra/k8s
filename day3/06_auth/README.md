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

# TOKEN Auth

kubectl -n kube-system describe secret default

`export token=`

```sh
TOKEN=$(kubectl exec -ti my-pod-reader -- cat /run/secrets/kubernetes.io/serviceaccount/token)
curl -k -H "Authorization: Bearer $TOKEN" https://192.168.0.170:6443/api
curl -k -H "Authorization: Bearer $TOKEN" https://192.168.0.170:6443/api/v1
curl -k -H "Authorization: Bearer $TOKEN" https://192.168.0.170:6443/api/v1/namespaces/default/pods
```


# User

```sh
openssl genrsa -out maciej.key 2048
openssl req -new -key maciej.key -out maciej.csr -subj "/CN=maciej/O=workshop"
```

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: maciej
spec:
  groups:
  - system:authenticated
  request:  # replace with output from shell command: cat maciej.csr | base64 | tr -d '\n'
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
```

```sh
kubectl get csr
kubectl certificate approve maciej
kubectl get csr maciej -o jsonpath='{.status.certificate}'| base64 -d > maciej.crt

```


```
kubectl config set-credentials maciej --client-certificate=maciej.crt  --client-key=maciej.key
kubectl config set-context maciej-context --cluster=docker-desktop --namespace=default --user=maciej
kubectl --context=maciej-context get pods
kubectl create namespace workshop
```

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: workshop
  name: deployment-manager
rules:
- apiGroups: ["", "extensions", "apps"]
  resources: ["deployments", "replicasets", "pods"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"] # You can also use ["*"]
```

```yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: deployment-manager-binding
  namespace: workshop
subjects:
- kind: User
  name: maciej
  apiGroup: ""
roleRef:
  kind: Role
  name: deployment-manager
  apiGroup: ""
```

```sh
kubectl --context=maciej-context get pods --namespace=workshop
```
