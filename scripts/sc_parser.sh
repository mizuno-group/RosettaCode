#!/bin/bash

source /opt/pip-env/bin/activate
SCOREDIR=$1

for SC in ${SCOREDIR}/*.sc; do
    FILEPATH=$(cd $(dirname $0);pwd)
    python3 ${FILEPATH}/sc_parser.py "${PWD}/${SC}"
    rm ${SC}
done
