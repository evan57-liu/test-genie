from fastapi import APIRouter, Request, Depends

from test_genie.app.container import Container
from test_genie.app.dto.user_dto import LoginRequest, LoginResponse

user_router = APIRouter(prefix="/users", tags=["User"])


def get_user_service():
    return Container.user_service


@user_router.post(
    "/login",
    response_model=LoginResponse,
    summary="login",
)
async def login(req: Request, login_reqeust: LoginRequest, user_service=Depends(get_user_service)):
    return await user_service.login(req, login_reqeust)
