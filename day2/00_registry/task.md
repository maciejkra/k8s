# Run registry container

1. image name: `registry`
2. image version: `2`
3. forward port to `5000` port in registry

# Curl should work

`curl <host_ip>:<forwarded_port>/v2/_catalog`

expected result
```js
{"repositories":[]}
```

# Tag one of your previous images to match 

Use 127.0.0.1 address!

```sh
docker image tag <??>
```

# Push image to new repostiory

Expected result after completed task

`curl <host_ip>:<forwarded_port>/v2/_catalog`

expected result
```js
{"repositories":["YOUR_IMAGE"]}
```

# Using IP of host without tls

`vim /etc/docker/daemon.json`
```daemon.json
{"insecure-registries":["192.168.0.125:5000"]}
```

```sh
systemctl restart docker
docker container start registry
```

# Consider 

1. Restart container when docker starts `--restart=always`
2. volume mount at: `/var/lib/registry`

For more production case read:
1. https://docs.docker.com/registry/deploying/
2. https://docs.docker.com/registry/configuration/#letsencrypt