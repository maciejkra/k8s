docker image build -t my-volume ./01_volume_ls
docker volume ls
docker container run --rm my-volume
docker container run my-volume
docker volume ls
touch /tmp/something
docker container run --rm -v /tmp:/data my-volume /data


# Create volume and add :ro flag
docker volume create my-volume
docker run -v my-volume:/data:ro --name container1 -d my-nginx
docker run -v my-volume:/data -d --name container2 my-nginx

docker exec -it container1 sh
touch /data/plik
exit

docker exec -it container2 sh
touch /data/plik
exit


