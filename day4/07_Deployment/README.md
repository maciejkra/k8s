https://github.com/ContainerSolutions/k8s-deployment-strategies


## Task

1. Create 2 different Deployments with nginx
2. Attach volume to each of those
3. For one deployment create index.htm file saying `new version` and `old version` for another
4. Both deployments should have different names but same match labels
5. Create service for this deployment
6. Create ingress attached to this service
7. Access through browser, traffic should hit both of them 50% of time
