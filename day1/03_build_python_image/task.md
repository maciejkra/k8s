# Create new Dockerfile on your own 

- Use base image `python:3-slim`
- Set working dir (`Workdir`) to `/usr/src/app`
- execute command in image `pip install --no-cache-dir -r requirements.txt`
- allow port access on `5002`
- copy main.py & requirements.txt files
- copy api folder
- add env variable called `LOG_LEVEL` with value `INFO`
- run command `python` and `main.py`

# Run container form builded image
1. Check container port
2. Verify with curl endpoint

`curl localhost:<port_number>/healthz`

# Connect apps

1. Run container from image `redis` and expose it on port 6379 targeting 6379 port in container
2. Run python one more time with env parameter

`docker container run -e REDIS_HOST=<host_ip> -d -P my-python`

3. Check python can connect

```sh
localhost:32771/healthz
curl localhost:32771/api/v1/info
curl -XPOST localhost:32771/api/v1/info
curl localhost:32771/api/v1/info
```

3. Update env LOG_LEVEL to DEBUG in run command


check difference ing logs