package main

import (
    "context"
    "log"
    "os"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials"
    pb "go-client/protos"
)

func getEnv(key, fallback string) string {
    if value, ok := os.LookupEnv(key); ok {
        return value
    }
    return fallback
}

func tls_client(target string) {
    // 需要设置 GODEBUG="x509ignoreCN=0"
    // TLS连接
    creds, err := credentials.NewClientTLSFromFile("../mygrpc/keys/cert.pem", "grpc.seekplum.top")
    if err != nil {
        log.Fatalf("Failed to create TLS credentials %v", err)
        return
    }

    // 连接服务器
    conn, err := grpc.Dial(target, grpc.WithTransportCredentials(creds))
    if err != nil {
        log.Printf("连接服务端失败: %s", err)
        return
    }
    defer conn.Close()
    // 新建一个客户端
    c := pb.NewHelloServiceClient(conn)
    // 调用服务端函数
    r, err := c.Hello(context.Background(), &pb.HelloRequest{Name: "TLS go-test123"})
    if err != nil {
        log.Printf("调用服务端代码失败: %s", err)
        return
    }
    log.Printf("调用成功: %s", r.Message)
}

func normal_client(target string) {
    // 连接服务器
    // conn, err := grpc.Dial(target, grpc.WithInsecure())
    conn, err := grpc.DialContext(context.TODO(), target, grpc.WithInsecure())
    if err != nil {
        log.Printf("连接服务端失败: %s", err)
        return
    }
    defer conn.Close()
    // 新建一个客户端
    c := pb.NewHelloServiceClient(conn)
    // 调用服务端函数
    r, err := c.Hello(context.Background(), &pb.HelloRequest{Name: "go-test123"})
    if err != nil {
        log.Printf("调用服务端代码失败: %s", err)
        return
    }
    log.Printf("调用成功: %s", r.Message)
}

func main(){
    target := getEnv("CHANNEL_SERVER_TARGET", "0.0.0.0:8086")
    is_secure := false
    if getEnv("CHANNEL_SERVER_SECURE", "tls") == "tls" {
        is_secure = true
    }
    if is_secure {
        tls_client(target)
    } else {
        normal_client(target)
    }
}
