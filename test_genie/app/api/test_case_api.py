from fastapi import APIRouter, Request, Depends

from test_genie.app.container import Container
from test_genie.app.dto import CommonResponse
from test_genie.app.dto import success_response
from test_genie.app.dto.testcase_dto import GenerateTestCaseRequest, GenerateTestCaseResponse, TestCaseDto, \
    GetTestCasesResponse

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
    "/file/{file_id}",
    response_model=TestCaseDto,
    summary="get test case",
)
async def get_test_case(req: Request, file_id: int, testcase_service=Depends(get_testcase_service)):
    return await testcase_service.get_test_case(req, file_id)


@testcase_router.get(
    "/user/{user_id}",
    response_model=GetTestCasesResponse,
    summary="get test cases",
)
async def get_test_cases(req: Request, user_id: int, testcase_service=Depends(get_testcase_service)):
    return await testcase_service.get_test_cases(req, user_id)


@testcase_router.delete(
    "/{test_case_id}",
    response_model=CommonResponse,
    summary="delete test case",
)
async def delete_test_case(req: Request, test_case_id: int, testcase_service=Depends(get_testcase_service)):
    await testcase_service.delete_test_case(req, test_case_id)
    return success_response()
