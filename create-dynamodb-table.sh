#!/bin/bash

set -x

aws dynamodb create-table --table-name lots-of-lists \
  --attribute-definitions AttributeName=userId,AttributeType=S AttributeName=listId,AttributeType=S \
  --key-schema AttributeName=userId,KeyType=HASH AttributeName=listId,KeyType=RANGE \
  --provisioned-throughput ReadCapacityUnits=2,WriteCapacityUnits=2 \
  --endpoint-url=http://localhost:8000
