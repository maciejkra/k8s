# Recreate Python+Redis on Kubernetes

1. Create Deployment yaml file for `redis:alpine`
1. Create Deployment yaml file for `krajewskim/python-api:new`
1. Create service yaml file for redis with ClusterIP type. **Don't call it redis**
1. Create service yaml file for python with NodePort type. **Call it python-service**
1. Set `LOG_LEVEL` env to `DEBUG` for python deployment
1. Set `REDIS_HOST` env to name of `redis service` for python deployment
1. Make sure all ports are correct (REDIS=6379 PYTHON-API=5002)
1. Use proper labels
1. Create everything at once with:

```sh
kubectl apply -f .
```

# check everything works 

```sh
curl 127.0.0.1:32000/api/v1/info
curl -XPOST 127.0.0.1:32000/api/v1/info
curl 127.0.0.1:32000/api/v1/info
```
NOTE: your IP address and port my vary - please check it.