#!/usr/bin/env bash

mongoimport -h ds045622.mongolab.com:45622 \
    -u yeqing \
    -p password \
    -d mymongo \
    -c "$1"} \
    --file $1.osm.json
