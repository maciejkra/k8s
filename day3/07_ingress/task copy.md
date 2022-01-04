1. Create ingress for python 
python.127.0.0.1.nip.io
you should be able to access python at

kubernetes.docker.internal/python/healthz

1. Create config map with redis host: <redis-service-name> 
2. Use config map in python deployment to set REDIS_HOST
3. Use volumes in redis deployment to attach volume to `/data` folder