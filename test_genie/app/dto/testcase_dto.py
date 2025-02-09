from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from test_genie.app.enums import TestCaseStatus
from test_genie.app.dto.file_dto import FileDto


class GenerateTestCaseRequest(BaseModel):
    file_id: int = Field(..., description="File ID")
    prompt: Optional[str] = Field(default=None, description="Prompt")


class GenerateTestCaseResponse(BaseModel):
    test_case_id: int = Field(..., description="Test Case ID")


class GetTestCasesResponse(BaseModel):
    test_cases: List["TestCaseDto"]


class TestCaseDto(BaseModel):
    id: int = Field(default=None, description="Test Case ID")
    result: Optional[str] = Field(..., description="Result")
    status: TestCaseStatus = Field(..., description="Status")
    file_id: int = Field(..., description="File ID")
    created_at: datetime = Field(default=None, description="Created At")
    updated_at: datetime = Field(default=None, description="Updated At")
    file: Optional["FileDto"] = Field(default=None, description="File")
