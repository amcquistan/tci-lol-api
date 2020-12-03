#!/bin/bash

set -x

sam local start-api --parameter-overrides ExecEnv=local --docker-network dynamodb-local

