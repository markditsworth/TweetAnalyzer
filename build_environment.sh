#!/bin/bash

cd ./kafka
./run.sh

cd ../elasticsearch
./run.sh

sleep 5

cd ../kibana
./run.sh


cd ../logstash
./run.sh
