# Create pods

```sh
kubectl apply -f pod-config.yaml
kubectl logs configmap-pod
kubectl logs configmap-pod | grep line
```

```sh
kubectl apply -f pod-config-volume.yaml
kubectl logs configmap-volume-pod
```

# Autoupdates for mounted configmaps
```sh
kubectl edit configmap configuration
# change service-b.config
kubectl logs -f configmap-volume-pod
```

# Worth Checking
https://github.com/stakater/Reloader
