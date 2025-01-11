from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class GetDefaultResponse(BaseModel):
    prompt: str = Field(..., description="prompt")
