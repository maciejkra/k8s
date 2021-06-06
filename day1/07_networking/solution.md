# Remove old stuff
docker container rm -f my-redis
docker container rm -f  my-python-service

# Create

docker network ls
docker network create python-redis-network
docker container run --network python-redis-network -d --name my-redis redis:5.0.10
docker container run --network python-redis-network -d -P -e REDIS_HOST=my-redis --name my-python-service my-python
docker container exec -ti  my-python-service curl 127.0.0.1:5002/api/v1/info
docker container exec -ti  my-python-service curl -XPOST 127.0.0.1:5002/api/v1/info
docker container exec -ti  my-python-service curl 127.0.0.1:5002/api/v1/info

# Data

ID=$(docker container inspect -f "{{ (index .Mounts 0).Name }}" my-redis)
docker volume inspect $ID
docker container stop my-redis
docker container rm my-redis
docker image inspect -f "{{.ContainerConfig.Volumes}}"  redis:5.0.10
docker container run --network python-redis-network -d --name my-redis -v $ID:/data redis:5.0.10
docker container exec -ti  my-python-service curl 127.0.0.1:5002/api/v1/info

# Clean
docker container stop  my-redis
docker container stop my-python-service
docker container prune -f
docker volume prune -f
