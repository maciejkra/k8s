# Compose

Compose is a tool for defining and running multi-container Docker applications. It takes
declarative approach to provide working containers with a managed sets.

```sh
sudo apt install docker-compose
```

# Compose task

in `01_build` run `docker-compose up -d`

verify running service

`docker-compose ps`

# Create compose file for nginx, python, redis

1. Web (nginx) service
- create index.htm and mount with `volumes` in yaml to `/usr/share/nginx/html/`
- use image `nginx:1.15.5`

2. Python service
- add service with `my-python` image and expose on port `5002`
- add `depends_on:` to python to depend on redis
- scale service `docker-compose up -d --scale web=3`
- `docker-compose down` stops & removes all stuff (see help)
- run single service `docker-compose up -d python`, should start redis
- `docker-compose exec python curl web` should access created index.html
- `docker-compose logs`
- `docker-compose logs -f web`

execute multiple curls to web

# check containers 

enter into service

```sh
docker-compose exec web /bin/bash
```

# Load balancing

- remove port forward
- scale web
- execute curl from python to web `docker-compose exec pyredis curl web`
- see logs for web from docker-compose
- see logs directly from docker
