from fastapi import Request
from markitdown import MarkItDown

from test_genie.core.exceptions import BadRequestException
from test_genie.app.models import File, TestCase
from test_genie.app.enums import TestCaseStatus
from test_genie.app.dto.testcase_dto import GenerateTestCaseRequest, GenerateTestCaseResponse, TestCaseDto
from test_genie.app.prompt import prompt


class TestCaseService:
    def __init__(self, session_factory, openai_client):
        self.session_factory = session_factory
        self.openai_client = openai_client

    async def get_test_case(self, req: Request, test_case_id: int) -> TestCaseDto:
        with self.session_factory() as session:
            test_case = session.query(TestCase).filter(TestCase.id == test_case_id).scalar()
            if not test_case:
                raise BadRequestException("test case not found")

        return TestCaseDto(
            id=test_case.id,
            result=test_case.result,
            status=test_case.status,
            file_id=test_case.file_id,
            created_at=test_case.created_at,
            updated_at=test_case.updated_at
        )

    async def generate_test_case(self, req: Request, body: GenerateTestCaseRequest) -> GenerateTestCaseResponse:
        with self.session_factory() as session:
            file = session.query(File).filter(File.id == body.file_id).scalar()
            if not file:
                raise BadRequestException("file not found")

        if file.name.endswith(".md"):
            content = read_md_file(file.path)
        else:
            content = read_other_file(file.path)

        try:
            test_case_result = self._generate_test_case(body.prompt, content)
        except Exception as e:
            with self.session_factory() as session:
                test_case = TestCase(file_id=body.file_id, status=TestCaseStatus.FAILED)
                session.add(test_case)
            raise e

        with self.session_factory() as session:
            test_case = TestCase(file_id=body.file_id, status=TestCaseStatus.SUCCESS, result=test_case_result)
            session.add(test_case)

        # with self.session_factory() as session:
        #     test_case.result = test_case_result
        #     test_case.status = TestCaseStatus.SUCCESS
        #     session.commit()

        return GenerateTestCaseResponse(test_case_id=test_case.id)

    def _generate_test_case(self, p: str, content: str) -> str:
        if not p or p.strip() == "":
            p = prompt

        completion = self.openai_client.chat.completions.create(
            model="chatgpt-4o-latest",
            max_tokens=16384,
            temperature=0.2,
            top_p=0.95,
            messages=[
                {"role": "system", "content": p},
                {
                    "role": "user",
                    "content": content
                }]
        )

        return completion.choices[0].message.content


def read_md_file(file_path: str) -> str:
    """
    读取 .md 文件的内容
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def read_other_file(file_path: str) -> str:
    """
    读取 .docx 文件的内容
    """
    md = MarkItDown()
    result = md.convert(file_path)

    return result.text_content
