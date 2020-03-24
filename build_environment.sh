#!/bin/bash

echo -n "Building Kafka..."
cd ./kafka
./run.sh
echo "     Done."
echo

echo -n "Building Elasticsearch..."
cd ../elasticsearch
./run.sh
sleep 5
echo "     Done."
echo

echo -n "Building Kibana..."
cd ../kibana
./run.sh
echo "     Done."
echo

echo -n "Building Logstash pipeline..."
cd ../logstash
./run.sh
echo "     Done."
echo "Ready for tweets!"
