#!/bin/bash

docker network create kafka-network --driver bridge

sleep 10

docker run -d --name zk-server --network kafka-network -e ALLOW_ANONYMOUS_LOGIN=yes zookeeper

sleep 15

docker run -d --name kafka-server --network kafka-network -e ALLOW_PLAINTEXT_LISTENER=yes -e KAFKA_CFG_ZOOKEEPER_CONNECT=zk-server:2181 -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,PLAINTEXT_HOST://:29092 -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-server:9092,PLAINTEXT_HOST://localhost:29092 -p 9092:9092 -p 29092:29092 kafka

