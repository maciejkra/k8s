# Docker Compose Demo

This demo using docker-compose to bring up a complete stack with the demo app, including Grafana, Prometheus, Loki and Tempo.
The datasources and cross-datasource links should all be configured correctly.

To run:

```shell
$ ARCH=$(docker info --format '{{.Architecture}}' | sed 's/x86_64/amd64/;s/aarch64/arm64/')
$ docker plugin install grafana/loki-docker-driver:3.7.7-$ARCH --alias loki --grant-all-permissions
$ docker compose up -d
```

The navigate to http://localhost:3000 to see Grafana.

## Fancy Query
```
{job="tns/app"} | logfmt | status>=500 and status <=599 and duration > 50ms
```