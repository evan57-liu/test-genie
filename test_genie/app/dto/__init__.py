from pydantic import BaseModel


class CommonResponse(BaseModel):
    code: int = ""
    message: str = ""


def success_response() -> CommonResponse:
    return CommonResponse(message='success')
