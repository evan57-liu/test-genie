from fastapi import APIRouter

from test_genie.app.dto import success_response
from pydantic._internal._config import ConfigWrapper

health_router = APIRouter(prefix="/test", tags=["Health"])


@health_router.get(
    "/ping",
    summary="health check"
)
async def ping():
    return success_response()


@health_router.post(
    "/ping",
    summary="health check"
)
async def ping():
    return success_response()
