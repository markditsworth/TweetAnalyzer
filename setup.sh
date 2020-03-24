#!/bin/bash

echo "Install Zookeeper and Kafka container images..."
cd ./kafka
./init.sh

echo "Install logstash container image..."
cd ../logstash
./init.sh

echo "Install elasticseach container image..."
cd ../elasticsearch
./init.sh

echo "Install kibana container image..."
cd ../kibana
./init.sh

echo "Install python environment..."
cd ../python
./create_twitter_venv.sh
