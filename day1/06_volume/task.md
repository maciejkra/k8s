# Volumes

## display volume

`docker volume ls`

# Attach volume

1. Build image from `01_volume_ls`
2. Run container 
3. `touch /tmp/something`
3. Run container with `-v /tmp:/data <image_name> /data`

File something should be displayed

# Create new Dockerfile

1. Create new Dockerfile
2. Base image on previous
3. Change CMD to execute `"ls", "-la","/data"`

# Create volume and add :ro flag

1. Create volume `docker volume create my-volume`
2. List new volume
3. Run 2 containers with `my-nginx` image

First with `-v my-volume:/data:ro`
Second with `-v my-volume:/data`

4. Exec into second container and create new file in `/data` folder
5. Verify first container can read file
6. Verify first container can't write file to `/data`