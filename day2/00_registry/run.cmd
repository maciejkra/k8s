docker container run -d --name registry -p 5000:5000 registry:2
docker tag  src_image_name 127.0.0.1:5000/rewrwerew
docker push