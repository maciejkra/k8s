#!/bin/bash
docker container create --name mycpp scratch-hello-world-example
docker container cp mycpp:/main hello_from_container
