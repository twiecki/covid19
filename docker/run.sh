#!/usr/bin/env bash
echo "Running covid19 docker image from fabiononato/covid19"
docker run -it --rm --name tf2-gpu-covid -v $(pwd):/tf -p 8888:8888 -p 8000:8000 fabiononato/covid19:latest 
