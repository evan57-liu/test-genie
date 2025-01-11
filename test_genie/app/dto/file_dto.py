from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UploadFileResponse(BaseModel):
    file_id: int = Field(..., description="File ID")
    file_name: str = Field(..., description="File Name")


class GetFilesResponse(BaseModel):
    files: List["FileDto"] = Field(..., description="Files")


class FileDto(BaseModel):
    id: int = Field(..., description="File ID")
    name: str = Field(..., description="File Name")
    user_id: int = Field(..., description="User ID")
    created_at: Optional[datetime] = Field(default=None, description="Created At")
    updated_at: Optional[datetime] = Field(default=None, description="Updated At")
