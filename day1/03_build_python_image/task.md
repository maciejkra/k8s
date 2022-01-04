# Create new Dockerfile on your own 

- Use base image `python:3-alpine`
- Set working dir (`WORDKIR`) to `/usr/src/app`
- allow port access on `5002`
- copy main.py & requirements.txt files
- execute command in image `pip install --no-cache-dir -r requirements.txt`
- add env variable called `LOG_LEVEL` with value `INFO`
- run command `uvicorn main:app --host 0.0.0.0 --port 5002`

# Run container form builded image
1. Check container port
2. Verify with curl endpoint

`curl localhost:<port_number>/healthz`

# Connect apps

1. Run container from image `redis`
2. Run python one more time with env parameter

`docker container run -e REDIS_HOST=<host_ip> -d -P my-python`

3. Check python can connect

```sh
localhost:<port>/healthz
curl localhost:<port>/api/v1/info
curl -XPOST localhost:<port>/api/v1/info
curl localhost:<port>/api/v1/info
```

3. Update env LOG_LEVEL to DEBUG in run command


check difference in logs
