#!/bin/bash

set -xe

ROOT_DIR="$( cd "$( dirname "$BASH_SOURCE[0]" )" && pwd )"
cd "${ROOT_DIR}"
echo "Compiling protos..."

# # 生成 RSA 私钥
# openssl genrsa -out key.pem 2048

# # 生成 RSA 公钥, 除 Common Name 处必须填入 grpc.seekplum.top (和 grpc.ssl_target_name_override 变量一致) 外，其它直接回车即可
# openssl req -new -x509 -key key.pem -out cert.pem -subj "/CN=grpc.seekplum.top"
# # openssl req -new -x509 -sha256 -key key.pem -out cert.pem -days 3650 -subj "/CN=grpc.seekplum.top"

# cat key.pem cert.pem > mitm.pem


openssl genrsa -out rootCA.key 4096 -subj "/CN=grpc.seekplum.top"
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt
openssl genrsa -out localhost.key 2048
openssl req -new -key localhost.key -out localhost.csr -subj "/CN=grpc.seekplum.top"
openssl req -in localhost.csr -noout -text
openssl x509 -req -in localhost.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out localhost.crt -days 500 -sha256
openssl x509 -in localhost.crt -text -noout
cat localhost.crt localhost.key > localhost.pem
