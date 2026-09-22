# Remove old stuff
docker container rm -f my-redis
docker container rm -f  my-python-service

# Create

docker network ls
docker network create python-redis-network
docker container run --network python-redis-network -d --name my-redis redis
docker container run --network python-redis-network -d -p 5002:5002 -e REDIS_HOST=my-redis --name my-python-service my-python
curl 127.0.0.1:5002/api/v1/info
curl -XPOST 127.0.0.1:5002/api/v1/info
curl 127.0.0.1:5002/api/v1/info
