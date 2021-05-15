#!/bin/bash

set -e

ROOT_DIR="$( cd "$( dirname "$BASH_SOURCE[0]" )" && pwd )"
cd "${ROOT_DIR}"
echo "Compiling protos..."

# grpc的代码生成，生成Golang代码前需要安装 protoc-gen-go
if [ `type protoc-gen-go >/dev/null 2>&1 && echo 1 || echo 0` == "0" ]
then
    go get -u github.com/golang/protobuf/protoc-gen-go
fi

protoc -I../mygrpc/protos/ --go_out=plugins=grpc:. ../mygrpc/protos/*.proto
