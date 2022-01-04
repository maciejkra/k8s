https://helm.sh/docs/intro/install/

```sh
curl https://get.helm.sh/helm-v3.7.1-linux-amd64.tar.gz -o helm-v3.7.1-linux-amd64.tar.gz
tar -zxvf helm-v3.7.1-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
```

```sh
helm template --output-dir=./output .
helm template --output-dir=./output --values ./production.values.yaml .

```

```sh
kubectl create ns mynamespace
helm install . --generate-name
helm ls

kubectl config set-context --current=true --namespace=mynamespace
kubectl get all

kubectl config set-context --current=true --namespace=default
helm uninstall <>
helm upgrade --install --atomic my-release .

kubectl get all -n mynamespace
kubectl get secrets -n mynamespace

```

## other approach :)

https://artifacthub.io/

```sh
helm search hub wordpress
helm install happy-panda bitnami/wordpress

helm repo add bitnami https://charts.bitnami.com/bitnami
helm install happy-panda bitnami/wordpress
```

Customize values
```sh
helm show values bitnami/wordpress
echo '{mariadb.auth.database: user0db, mariadb.auth.username: user0}' > values.yaml
helm install -f values.yaml bitnami/wordpress --generate-name
helm get values happy-panda
```

Upgrade
```sh
helm upgrade -f panda.yaml happy-panda bitnami/wordpress
helm rollback happy-panda 1
```

https://helm.sh/docs/topics/charts/

Pro
```sh
helm create deis-workflow
```