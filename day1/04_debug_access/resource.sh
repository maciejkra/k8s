#!/bin/bash
docker run --rm -ti -d --name nginx-resource --cpu-shares 512 -m=100m monitoringartist/docker-killer cpubomb
