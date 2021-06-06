## Build image

```sh
docker image build -t my-hello-world .
```

## Check images

```sh
docker image ls 
```

## Find by label

```sh
docker image ls -f label=imagetype=workshops
```

# TASK PART

1. Run container from image
2. Run container and insert your name as last argument
3. Find container logs by container id
4. Remove container by id