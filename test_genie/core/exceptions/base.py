from pydantic import BaseModel, Field
from fastapi import HTTPException


class CustomException(HTTPException):
    def __init__(self, status_code=500, message="Internal Server Error"):
        self.message = message
        super().__init__(status_code=status_code, detail=message)


class ExceptionResult(BaseModel):
    code: int = Field(default=500, description="code")
    message: str = Field(default="An unexpected error occurred", description="message")
