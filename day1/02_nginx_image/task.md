# TASK

1. Build nginx image from parent folder
```sh
docker image build -t my-nginx -f nginx/Dockerfile nginx/
```

2. Run nginx container from previous step
3. Remove container
4. Create file `password` in nginx folder
5. Build image one more time
6. Run container with `-d` flag

# Exec container

1. enter container
```sh
docker container exec -ti <container_name> /bin/sh
```
2. Navigate to ` /usr/html` folder and list files

# Ignore files

Create `.dockerignore`

```.dockerignore
Dockerfile
password
```

1. Rebuild image but add tag version to it:

```sh
docker image build -t my-nginx:1 -f nginx/Dockerfile nginx/
```
2. Run container one more time
3. Verify that password file is no longe there

# Forward port

You can force remove container that is running

```sh
docker container rm -f my-nginx
```

1. Run container one more time using `-p` flag to forward port

```sh
docker container run --name my-nginx -p 8080:80 -d my-nginx
curl localhost:8080
```

# Forward port dynamicaly

1. Add to Dockerfile 

```Dockerfile
EXPOSE 80
```

2. Rebuild image & run container one more time with dynamic port assginment

```sh
docker container run --name my-nginx -P -d my-nginx
```

3. Verify what port was assigned

```sh
docker container port my-nginx
```

access port
```sh
curl localhost:32768
```

4. Finaly remove containers created in this task



