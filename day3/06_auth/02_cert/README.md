# User - CERT

```sh
openssl genrsa -out maciej.key 2048
openssl req -new -key maciej.key -out maciej.csr -subj "/CN=maciej/O=workshop"
```

Modify csr request
```
kubectl apply -f csr.yaml
```

Approve request
```sh
kubectl get csr
kubectl certificate approve maciej
kubectl get csr maciej -o jsonpath='{.status.certificate}'| base64 -d > maciej.crt

```

Add configuration

```
kubectl config set-credentials maciej --embed-certs --client-certificate=maciej.crt  --client-key=maciej.key
kubectl config set-context maciej-context --cluster=docker-desktop --namespace=default --user=maciej
kubectl --context=maciej-context get pods
kubectl create namespace workshop
```

Add role
```sh
kubectl apply -f role.yaml
kubectl apply -f rbac.yaml
```
Add configuration

```sh
kubectl --context=maciej-context get pods --namespace=workshop
```

