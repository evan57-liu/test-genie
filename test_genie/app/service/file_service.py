from datetime import datetime
import os

from fastapi import Request

from test_genie.core.exceptions import NotFoundException
from test_genie.app.models import File, User
from test_genie.app.dto.file_dto import UploadFileResponse, FileDto, GetFilesResponse


class FileService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_files(self, req: Request, user_id: int) -> GetFilesResponse:
        with self.session_factory() as session:
            files = session.query(File).filter(File.user_id == user_id).all()

        files_dto = []
        for file in files:
            files_dto.append(FileDto(
                id=file.id,
                name=file.name,
                user_id=file.user_id,
                created_at=file.created_at,
                updated_at=file.updated_at)
            )

        return GetFilesResponse(files=files_dto)

    async def upload_file(self, req: Request, user_id: int, file) -> UploadFileResponse:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).scalar()
            if not user:
                raise NotFoundException("user not found")

        file_path = f"./files/{datetime.now()}-{file.filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        f = File(name=file.filename, path=file_path, user_id=user_id)
        with self.session_factory() as session:
            session.add(f)

        return UploadFileResponse(file_id=f.id, file_name=f.name)
