#!/bin/bash

network=`docker network ls | grep kafka-network`

if [ -z ${network} ]; then
        echo "creating docker network..."
        flag=""
        docker network create kafka-network --driver bridge
        sleep 5
else
        flag="already"
fi
echo "Docker network ${flag} created."

zk=`docker ps -a | grep zk-server`
if [ -z ${zk} ]; then
	echo "spinning up zookeeper container..."
	flag=""
	docker run -d --name zk-server --network kafka-network -e ALLOW_ANONYMOUS_LOGIN=yes zookeeper
	sleep 5
else
	flag="already"
fi
echo "Zookeeper container ${flag} created."



kf=`docker ps -a | grep kafka-server`
if [ -z ${kf} ]; then
        echo "spinning up kafka container..."
        flag=""
	#docker run -d --name kafka-server --network kafka-network -e ALLOW_PLAINTEXT_LISTENER=yes -e KAFKA_CFG_ZOOKEEPER_CONNECT=zk-server:2181 -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,PLAINTEXT_HOST://:29092 -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-server:9092,PLAINTEXT_HOST://localhost:29092 -p 9092:9092 -p 29092:29092 kafka
	docker run -d --name kafka-server --network kafka-network -e ALLOW_PLAINTEXT_LISTENER=yes -v $(pwd)/server.properties:/opt/bitnami/kafka/conf/server.properties -p 9092:9092 -p 29092:29092 kafka
	sleep 5
else
        flag="already"
fi
echo "Kafka container ${flag} created."

