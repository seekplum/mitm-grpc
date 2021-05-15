FROM golang:1.15.5-alpine as build
WORKDIR /app
ENV GOPROXY https://mirrors.aliyun.com/goproxy
RUN apk add protoc
ADD ./go-client/go.mod .
ADD ./go-client/go.sum .
RUN go mod download
ADD ./go-client/gencode.sh .
ADD ./mygrpc /mygrpc
RUN mkdir protos && sh ./gencode.sh
ADD ./go-client/hello_client.go .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
FROM scratch
COPY --from=build /app/app /app/app
COPY --from=build /mygrpc/keys/cert.pem /mygrpc/keys/cert.pem
CMD [ "/app/app" ]
