Are used for *non-identifying* information

```json
"metadata": {
  "annotations": {
    "key1" : "value1",
    "key2" : "value2"
  }
}
```

```sh

kubectl annotate pod  $(kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}') workshop.test=verified
kubectl get pods $(kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}')  -o jsonpath='{.metadata.annotations}'
kubectl describe pods $(kubectl get pods -l app=myapp -o jsonpath='{.items[0].metadata.name}')  
```