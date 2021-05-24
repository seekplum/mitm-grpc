from mitmproxy import ctx, http, tcp
from mitmproxy.connections import ClientConnection, ServerConnection
from mitmproxy.net.http import Request
from mitmproxy.utils import strutils


def tcp_message(flow: tcp.TCPFlow):
    message: tcp.TCPMessage = flow.messages[-1]
    server_conn: ServerConnection = flow.server_conn
    client_conn: ClientConnection = flow.client_conn
    flag = "*" * 10
    extra_data: dict = {
        "client_conn.address": client_conn.address,
        "client_conn": client_conn,
        "server_conn.address": server_conn.address,
        "server_conn": server_conn,
    }
    if server_conn.address in [("mitmdump", 8080), ("127.0.0.1", "8080")]:
        server_conn.address = ("127.0.0.1", 80)
        content = strutils.bytes_to_escaped_str(message.content)
        extra_data.update(content=content)
        ctx.log.info(f"{flag} tcp_message: {extra_data} {flag}")


def http_connect(flow: http.HTTPFlow) -> None:
    r: Request = flow.request
    flag: str = "+" * 10
    # Python: grpc-httpcli/0.0 Golang: grpc-go/1.38.0
    user_agent: str = r.headers.get("User-Agent", "")
    agent_info: list = user_agent.split("/", 1)
    is_grpc_request: bool = len(agent_info) == 2 and agent_info[0].startswith("grpc-")
    extra_data: dict = {
        "user_agent": user_agent,
        "first_line_format": r.first_line_format,
        "method": r.method,
        "scheme": r.scheme,
        "authority": r.authority,
        "data": r.data,
    }
    if is_grpc_request:
        r.host = "grpc.seekplum.top"
        ctx.log.info(f"{flag} http_connect: {extra_data} {flag}")


def request(flow: http.HTTPFlow) -> None:
    r: Request = flow.request
    host: str = r.pretty_host
    flag: str = "#" * 10
    ctx.log.info(f"{flag} request host: {host} {flag}")
    if host in ["web.seekplum.top"]:
        r.host, r.port = "127.0.0.1", 8088
        r.headers["Host"] = host
        return
    if host in ["mitmdump", "nginx", "grpc.seekplum.top"]:
        r.host, r.port = "127.0.0.1", 80
        r.headers["Host"] = "grpc.seekplum.top"
        return
