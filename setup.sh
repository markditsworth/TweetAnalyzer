#!/bin/bash

echo "Install Zookeeper and Kakfa container images..."
cd ./kafka
./init.sh

echo "Install Logstash container image..."
cd ../logstash
./init.sh

echo "Install Elasticsearch container image..."
cd ../elasticsearch
./init.sh

echo "Install Kibana container image..."
cd ../kibana
./init.sh

echo "Setup Python twitter streaming environment"
cd ../python
./create_twitter_venv.sh
