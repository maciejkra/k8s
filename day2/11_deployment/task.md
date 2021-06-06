
1. Create registry deployment set using `registry:2` image
2. Attach service to this registry with type `NodePort`

3. Tag previous builded image and push it

```sh
docker image tag my-python 127.0.0.1:3200/my-python
docker image push 127.0.0.1:3200/my-python
```

4. access registry by node port

```sh
curl 127.0.0.1:32002/v2/_catalog
```
verify image is there

5. Create deployment with python flask application using image address from registry service
6. Verify healthz is responding