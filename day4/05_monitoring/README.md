# Metrics server

Make sure hostnames of workers are working, if not edit `/etc/hosts`

```sh
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

kubectl edit deployment metrics-server -n kube-system

```yml
    command:
    - /metrics-server 
    - --kubelet-preferred-address-types=InternalIP
    - --kubelet-insecure-tls
    - --secure-port=4443
    - --cert-dir=/tmp

dnsPolicy: ClusterFirst
hostNetwork: true
```

# Kube Prometheus

```sh
git clone https://github.com/coreos/kube-prometheus/
kubectl apply --server-side -f manifests/setup
until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
kubectl apply -f manifests/
```

# Minikube

```sh
minikube addons list
minikube addons enable metrics-server
```

