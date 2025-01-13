from fastapi import APIRouter, Request, Depends, File, UploadFile

from test_genie.app.container import Container
from test_genie.app.dto import CommonResponse
from test_genie.app.dto import success_response
from test_genie.core.exceptions import BadRequestException
from test_genie.app.dto.file_dto import UploadFileResponse, GetFilesResponse

file_router = APIRouter(prefix="/files", tags=["File"])


def get_file_service():
    return Container.file_service


@file_router.delete(
    "/{file_id}",
    response_model=CommonResponse,
    summary="delete file",
)
async def delete_file(req: Request, file_id: int, file_service=Depends(get_file_service)):
    await file_service.delete_file(req, file_id)
    return success_response()


@file_router.get(
    "/{user_id}",
    response_model=GetFilesResponse,
    summary="get files",
)
async def get_files(req: Request, user_id: int, file_service=Depends(get_file_service)):
    return await file_service.get_files(req, user_id)


@file_router.post(
    "/upload/{user_id}",
    response_model=UploadFileResponse,
    summary="upload file",
)
async def upload_file(req: Request, user_id: int, file: UploadFile, file_service=Depends(get_file_service)):
    if not file.filename.endswith((".docx", ".md")):
        raise BadRequestException("Only .docx and .md files are supported")
    if file.size > 1024 * 1024 * 10:
        raise BadRequestException("file size should be less than 10MB")

    return await file_service.upload_file(req, user_id, file)
