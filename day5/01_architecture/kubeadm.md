Setup multinode simple:

Instal docker
```sh
curl -fsSL https://get.docker.com | sh
sudo swapoff -a
sudo vim /etc/fstab # remove swap

sudo mkdir /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF
sudo systemctl enable docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

```sh
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system
```

Install kubeadm
```sh
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-mark hold kubelet kubeadm kubectl
```

# Install

`Make sure CIDR doesn't clash with host ip range!`

```sh
sudo kubeadm init --pod-network-cidr=192.168.0.0/16 --apiserver-advertise-address=<IP>
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config


kubectl apply -f https://docs.projectcalico.org/v3.11/manifests/calico.yaml
```

# One second node:
```sh
sudo kubeadm join 172.18.111.70:6443 --token
```

# On first node

```sh
kubectl get pods --all-namespaces
```
# Find token

```sh
kubeadm token create --print-join-command
```

# allow shedule on control plane

```sh
kubectl taint nodes --all node-role.kubernetes.io/master-
```
# Bug with CoreDNS

```sh
kubectl -n kube-system get deployment coredns -o yaml | \
  sed 's/allowPrivilegeEscalation: false/allowPrivilegeEscalation: true/g' | \
  kubectl apply -f -
```


# Reset

```sh
sudo kubeadm reset
sudo iptables -F && sudo iptables -t nat -F && sudo iptables -t mangle -F && sudo iptables -X
```

# In case of issues 

```sh
sudo systemctl stop kubelet
sudo systemctl stop docker
sudo iptables --flush
sudo iptables -tnat --flush
sudo systemctl start kubelet
sudo systemctl start docker
sudo ufw disable
sudo iptables -P FORWARD ACCEPT
```
