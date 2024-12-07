# Install 

prepare the nodes and lunch `preapre.sh` on each of them - it will prepare the nodes for installation


**Save the output `kubeadm join` commands**

Install Network driver - Cilium
https://docs.cilium.io/en/stable/gettingstarted/k8s-install-default/

```sh
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}

export KUBECONFIG=/etc/kubernetes/admin.conf
cilium install --version 1.16.4
```

# On first node

```sh
kubectl get pods --all-namespaces
```
# Find token

```sh
kubeadm token create --print-join-command
```
