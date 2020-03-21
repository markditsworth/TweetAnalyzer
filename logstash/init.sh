#!/bin/bash

docker pull docker.elastic.co/logstash/logstash:7.6.1
docker tag docker.elastic.co/logstash/logstash:7.6.1 logstash
