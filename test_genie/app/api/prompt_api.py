from fastapi import APIRouter, Request

from test_genie.app.dto.prompt_dto import GetDefaultResponse
from test_genie.app.prompt import prompt

prompt_router = APIRouter(prefix="/prompts", tags=["Prompt"])


@prompt_router.get(
    "",
    response_model=GetDefaultResponse,
    summary="get default prompt",
)
async def get_default(req: Request):
    return GetDefaultResponse(prompt=prompt)
