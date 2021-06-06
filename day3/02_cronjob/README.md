https://crontab.guru/#*/1_*_*_*_*

```sh
kubectl get cronjob
kubectl create -f cronjob.hello.yaml
kubectl get cronjob
kubectl get job -l origin=cron
kubectl get pod -l origin=cron-job
kubectl logs -l origin=cron-job
kubectl delete -f cronjob.hello.yaml
kubectl get job -l origin=cron
kubectl get pod -l origin=cron-job
```

Consider missing resources

CronJob can easly lock your node

K8S CronJob vs Application with internal scheduler

