#!/usr/bin/env bash
set -xe

# ROOT_DIR="$( cd "$( dirname "$BASH_SOURCE[0]" )" && pwd )"

docker compose -p mitm -f docker/docker-compose.yml $*
