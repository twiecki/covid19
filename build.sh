#!/usr/bin/env bash

echo "Building Image for COVID19 Project"
docker build . -f Dockerfile -t fabiononato/covid19:latest
echo "Pushing image for COVID19 Project"
docker push fabiononato/covid19:latest
