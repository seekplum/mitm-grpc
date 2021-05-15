from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def configure_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def catch_http_exception(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            content=dict(
                status_code=exc.status_code,
                error_msg=f"method: {request.method}, path: {request.url.path}, error: {exc.detail}",
            )
        )


app = FastAPI()
configure_error_handlers(app)


@app.get("/status")
def the_status():
    return PlainTextResponse(f"[FastAPI] OK!\n")


@app.get("/hello")
def hello(name=Query("-")):
    return PlainTextResponse(f"[FastAPI] Welcome to {name}\n")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8084,
        debug=True,
        access_log=True,
        log_level="debug",
        reload=True,
    )
