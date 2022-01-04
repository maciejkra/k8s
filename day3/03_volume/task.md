1. Create deployment for registry 

- use image `registry:2`
- registry listens on port 5000
- create pvc & pv
- mount pvc to `/var/lib/registry` path

2. Create service with node port

access its endpont:
```sh
curl http://127.0.0.1:31690/v2/_catalog
```
you should receive empty response

3. Tag image using registry address and port

```sh
docker image tag <image> <registry-address>:<port>/<image>
```

4. Update `/etc/docker/daemon.json` with unsecure registry

```json
{
  "registry-mirrors": [],
  "insecure-registries": ["192.168.0.171:31690"],
  "debug": true,
  "experimental": false
}
```

restart docker

5. Push image to new registry

```sh
docker image push <registry-address>:<port>/<image>
```

6. Access registry endpoint again

access its endpont:
```sh
curl http://127.0.0.1:31690/v2/_catalog
```
7. delete registry pod
8. After new pod is created you should still see registry images