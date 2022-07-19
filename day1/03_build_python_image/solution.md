# Init

docker image build -t my-python -f Dockerfile.solution .
docker container run --name my-python-service -P -d my-python
docker container port my-python-service
curl localhost:<port>/healthz 


# Redis
docker container run -d redis
docker container rm -f my-python-service
docker container run -e REDIS_HOST=192.160.0.2 -d -P -e LOG_LEVEL=DEBUG --name  my-python-service my-python

docker container port my-python-service
curl localhost:<port>/api/v1/info
curl -XPOST localhost:<port>/api/v1/info
curl localhost:<port>/api/v1/info
docker container logs my-python-service
