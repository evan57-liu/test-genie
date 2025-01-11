from fastapi import Request

from test_genie.app.dto.user_dto import LoginRequest, LoginResponse
from test_genie.core.exceptions import BadRequestException
from test_genie.app.models import User
from test_genie.core.configs import config


class UserService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def login(self, req: Request, login_request: LoginRequest) -> LoginResponse:
        if login_request.password != config.DEFAULT_PASSWORD:
            raise BadRequestException("Email or password is incorrect")

        with self.session_factory() as session:
            user = session.query(User).filter(User.email == login_request.email).first()
            if not user:
                user = User(email=login_request.email, password=config.DEFAULT_PASSWORD)
                session.add(user)

        return LoginResponse(user_id=user.id, email=user.email)
