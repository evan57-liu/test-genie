from fastapi import APIRouter, Request, Depends

from test_genie.app.container import Container
from test_genie.app.dto.testcase_dto import GenerateTestCaseRequest, GenerateTestCaseResponse, TestCaseDto

testcase_router = APIRouter(prefix="/testcases", tags=["TestCase"])


def get_testcase_service():
    return Container.testcase_service


@testcase_router.post(
    "/generate",
    response_model=GenerateTestCaseResponse,
    summary="generate test case",
)
async def generate_test_case(req: Request, body: GenerateTestCaseRequest,
                             testcase_service=Depends(get_testcase_service)):
    return await testcase_service.generate_test_case(req, body)


@testcase_router.get(
    "/{test_case_id}",
    response_model=TestCaseDto,
    summary="get test case",
)
async def get_test_case(req: Request, test_case_id: int, testcase_service=Depends(get_testcase_service)):
    return await testcase_service.get_test_case(req, test_case_id)
