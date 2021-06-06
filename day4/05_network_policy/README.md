By default, pods are non-isolated
An empty podSelector selects all pods in the namespace

## Create policy

```sh
kubectl create -f deny.network.policy.yaml
kubectl exec -ti nginx-stsf-0 -- curl stsf-service.default # wont work
kubectl delete -f deny.network.policy.yaml
kubectl exec -ti nginx-stsf-0 -- curl stsf-service.default #  work

```
# Docs

https://kubernetes.io/docs/concepts/services-networking/network-policies/
https://kubernetes.io/docs/concepts/cluster-administration/networking/

## Deep into network

ref: https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/
ref: https://thenewstack.io/hackers-guide-kubernetes-networking/

# Compare CNI

https://docs.google.com/spreadsheets/d/1qCOlor16Wp5mHd6MQxB5gUEQILnijyDLIExEpqmee2k/edit#gid=0
