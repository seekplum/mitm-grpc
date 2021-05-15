#!/bin/bash

set -e

ROOT_DIR="$( cd "$( dirname "$BASH_SOURCE[0]" )" && pwd )"
cd "${ROOT_DIR}"
echo "Compiling protos..."

# grpc的代码生成
python -m grpc_tools.protoc -I../../mygrpc/protos/ --python_out=./ --grpc_python_out=./ ../../mygrpc/protos/*.proto
