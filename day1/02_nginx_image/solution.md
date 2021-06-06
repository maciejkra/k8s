# Init
docker image build -t my-nginx -f nginx/Dockerfile nginx/
docker container run --name my-nginx my-nginx
<ctrl+c>
docker container rm my-nginx
touch nginx/password
docker image build -t my-nginx -f nginx/Dockerfile nginx/
docker container run --name my-nginx -d my-nginx

# Debug

docker container exec -ti my-nginx /bin/sh
docker container exec -ti my-nginx ls /usr/html

# Ignore

touch nginx/.dockerignore
echo "password" >> nginx/.dockerignore
docker container stop my-nginx
docker container  rm my-nginx
docker image build -t my-nginx -f nginx/Dockerfile nginx/
docker container run --name my-nginx -d my-nginx
docker container exec -ti my-nginx ls /usr/html


