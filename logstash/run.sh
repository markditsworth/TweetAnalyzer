#!/bin/bash
#Todo: add -d
docker run -it --name logstash --network kafka-network -v $(pwd)/logstash.yml:/usr/share/logstash/config/logstash.yml -v $(pwd)/pipeline.conf:/usr/share/logstash/pipeline/logstash.conf logstash
