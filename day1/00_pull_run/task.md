# Run first container

## Pull image hello-world

```sh
docker image pull hello-world
```

## Run container hello-world

```sh
docker container run --name <myname> --label=type=workshop hello-world
```

## List all containers

```sh
docker container ls
docker container ls -a
docker container ls -a -f status=exited
docker container ls -a -f label=type=workshop
```

## Check logs

```sh
docker container logs <myname|id>
``` 

## Remove

```sh
docker container rm <myname>
```