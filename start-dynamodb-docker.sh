#!/bin/bash

set -x

docker run --network dynamodb-local --name dynamodb -p 8000:8000 amazon/dynamodb-local

