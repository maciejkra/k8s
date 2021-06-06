Fetching metrics from Heapster is deprecated as of Kubernetes 1.11.
*metric server required*



https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/

```sh
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```