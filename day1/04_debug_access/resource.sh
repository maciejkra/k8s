#!/bin/bash
docker run --rm -ti -d --cpu-shares 512 -m=100m monitoringartist/docker-killer cpubomb
