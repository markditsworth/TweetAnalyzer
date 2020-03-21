#!/bin/bash

docker pull bitnami/kafka:latest
docker tag bitnami/kafka kafka
docker pull bitnami/zookeeper:latest
docker tag bitnami/zookeeper zookeeper

