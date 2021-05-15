# mitmproxy grpc

## 背景

测试环境只暴露了一个端口，是通过 mitmproxy 进行暴露的，其它服务都是通过指定 Host，在 mitmproxy 内部进行转发的。

## 目标

维持只暴露一个端口的情况下，把 gRPC 服务也暴露出来

## 环境准备

- 1.生成私有 CA

```bash
bash mygrpc/keys/genkey.sh
```

- 2.生成 gRPC Python 代码(本地调试需要)

```bash
bash app/protos/gencode.sh
```

## 启动服务

```bash
# build镜像
bash mygrpc/keys/genkey.sh && bash dco.sh build

# 关闭所有服务
bash dco.sh down --remove-orphans -v

# 强制重启服务
bash dco.sh up -d --force-recreate
```

## 测试 FastApi 代理

```bash
curl http://web.seekplum.top/test --proxy http://127.0.0.1:8081

curl http://web.seekplum.top/status --proxy http://127.0.0.1:8081
```

## 测试 Grpc 代理

```bash
bash dco.sh up python-client
```
