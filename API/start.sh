#!/bin/bash
app="worseapi"
docker build -t ${app} .
docker run -d -p 49500:80 \
    --name=${app} \
    -v $PWD:/app ${app}
