# Create kustomization for python service
1. create deplyments & services for python service in bases
2. create 2 enviornments test and prod
3. prod:
   1. set ingress routing to python service under python.127.0.0.1.nip.io
   2. change replicas set to 2 for python service
   3. deploy everything in namespace python
4. test:
   1. change the namespace to test
   2. deploy service on NodePort