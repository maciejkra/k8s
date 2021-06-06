# Canary Deployments with NGINX Ingress Controller
## Overview
This repository contains all resources that are required to test the canary feature of NGINX Ingress Controller. 

## Requirements
* Kubernetes cluster 
* NGINX Ingress Controller 0.21.0+

## Getting Started

### Canary Test Scenario
##### Prepare Manifests  
First of all, change the host definition in the ingress manifests ***deploy/prod-ingress.yaml*** and ***deploy/canary-ingress.yaml*** from canary-demo.example.com to your URL
  
##### Deploy production release  
Roll-out the stable version 1.0.0 to the cluster
```bash
$ make step-1
```
  
##### Run tests  
Execute the following commands to send n=1000 requests to the endpoint
```bash
$ ab -n 1000 -c 100 -s 60 "http://<your_URL>/version"
$ curl -s "http://<your_URL>/metrics" | jq '.calls'
```
If everything is working as expected, the curl command should return "1000".
  
##### Reset request counter  
Send GET requests to /reset endpoint to set the request counter to zero
```bash
$ curl "http://<your_URL>/reset"
```
  
##### Canary deployment  
Push the new software version 1.0.1 as a canary deployment to the cluster
```bash
$ make step-2
```
  
##### Perform tests  
Again, start sending traffic to the endpoint
```bash
$ ab -n 1000 -c 100 -s 60 "http://<your_URL>/version"
```
  
##### Verify the weight split  
Do a port forward to each of the pods to check the request count
```bash
$ kubectl -n demo-prod port-forward <pod-name> 8080:8080
$ curl -s http://localhost:8080/metrics | jq '.calls'
$ kubectl -n demo-prod port-forward <pod-name> 8081:8080
$ curl -s http://localhost:8081/metrics | jq '.calls'
```
Unless the weight has been changed to a different value, you should see approximately 800 requests being served by the production deployment and the remainig 200 by the canary. 

### Delete
Remove all resource from the cluster 
```bash
$ make clean-up
```
