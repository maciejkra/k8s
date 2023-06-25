https://helm.sh/docs/intro/install/

```sh
 helm template --output-dir=./output .
 helm template --output-dir=./output --values ./production.values.yaml .
 ```

```sh
helm install . --generate-name
helm ls

kubectl get all 


helm uninstall <?>
helm upgrade --install --atomic my-release .

# for the future use you might consider...
# helm upgrade --install --atomic my-release . --values production.values.yaml -n NAMESPACE --create-namespace 


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
echo '{mariadb.auth.database: user0db, mariadb.auth.username: user0}' > values.json
helm install -f values.jsons bitnami/wordpress --generate-name
helm get values happy-panda
```

Upgrade
```sh
helm upgrade -f values.jsons happy-panda bitnami/wordpress
helm rollback happy-panda 1
```

https://helm.sh/docs/topics/charts/

Pro
```sh
helm create deis-workflow
```
