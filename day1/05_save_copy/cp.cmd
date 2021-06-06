docker container create --name backup-container my-nginx
docker container cp backup-container:/usr/html/index.html ./
