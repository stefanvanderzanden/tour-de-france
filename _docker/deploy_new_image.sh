#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

docker build -f _docker/Dockerfile -t tour-de-france:test .
docker tag tour-de-france:test registry.digitalocean.com/svdzanden/tour-de-france:test
docker push registry.digitalocean.com/svdzanden/tour-de-france:test