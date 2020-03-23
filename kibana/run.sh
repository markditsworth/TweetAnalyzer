#!/bin/bash

docker run --name kibana --link elasticsearch:elasticsearch -p 5601:5601 kibana
