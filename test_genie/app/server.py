from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from test_genie.core.configs import config
from test_genie.core.exceptions import (
    CustomException,
    ExceptionResult,
)
from test_genie.core.fastapi.middlewares import LoggingMiddleware
from test_genie.app.container import Container
from test_genie.app.api import router


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(LoggingMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=make_middleware(),
    )
    init_routers(app_=app_)

    return app_


app = create_app()


@app.exception_handler(Exception)
async def custom_exception_handler(_: Request, ex: Exception):
    if isinstance(ex, CustomException):
        result = ExceptionResult(code=ex.status_code, message=ex.message)
    elif isinstance(ex, HTTPException):
        result = ExceptionResult(code=ex.status_code, message=ex.detail)
    elif isinstance(ex, Exception):
        result = ExceptionResult(code=500, message=str(ex))
    else:
        result = ExceptionResult()  # Uses default values
    logger.error(f"Error: {result.code} - {result.message}")

    return reset_response(JSONResponse(
        status_code=result.code,
        content={"code": result.code, "message": result.message},
    ))


# handle the validation error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc}")
    return reset_response(JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": status.HTTP_400_BAD_REQUEST, "message": exc.errors()[0]['msg']},
    ))


def reset_response(response: JSONResponse) -> JSONResponse:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response
