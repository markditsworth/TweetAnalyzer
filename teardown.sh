#!/bin/bash

docker rm -f kibana
docker rm -f elasticsearch
docker rm -f logstash
docker rm -f kafka-server
docker rm -f zk-server
docker network rm kafka-network
