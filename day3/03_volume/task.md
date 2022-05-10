To our previous deployment project (python-redis) add volume using storage class for redis (folder `/data`)
1. run yaml files and see if everything works:
```sh
curl python-service:5002/api/v1/info
curl -XPOST python-service:5002/api/v1/info
curl python-service:5002/api/v1/info
```
2. delete redis deployment and add it again (counter should show the old value)
