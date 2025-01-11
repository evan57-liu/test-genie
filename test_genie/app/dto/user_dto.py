from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")


class LoginResponse(BaseModel):
    user_id: int = Field(..., description="User ID")
    email: str = Field(..., description="Email")
