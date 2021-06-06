```sh
kubectl create -f redis.yaml
kubectl create -f producer.job.yaml
kubectl create -f parallel.job.yaml
kubectl get job
kubectl logs -f -l type=consumer
```

