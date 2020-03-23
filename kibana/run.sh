#!/bin/bash

docker run --name kibana --network kafka-network -v $(pwd)/kibana.yml:/usr/share/kibana/config/kibana.yml -p 5601:5601 kibana
