#!/usr/bin/env bash

echo "Building Image for COVID19 Project"
cp ../requirements.txt .
docker build . -f Dockerfile -t fabiononato/covid19:latest
docker rm requirements.txt
echo "Pushing image for COVID19 Project"
docker push fabiononato/covid19:latest
