docker image build -t my-volume ./01_volume_ls
docker volume ls
docker container run --rm my-volume
docker container run my-volume
docker volume ls
touch /tmp/something
docker container run --rm -v /tmp:/data my-volume /data


