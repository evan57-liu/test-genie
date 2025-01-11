from fastapi import APIRouter

from test_genie.app.api.health_api import health_router
from test_genie.app.api.file_api import file_router
from test_genie.app.api.user_api import user_router
from test_genie.app.api.prompt_api import prompt_router
from test_genie.app.api.test_case_api import testcase_router

router = APIRouter(prefix="/api/v1")
router.include_router(health_router, tags=["Health"])
router.include_router(file_router, tags=["File"])
router.include_router(user_router, tags=["User"])
router.include_router(prompt_router, tags=["Prompt"])
router.include_router(testcase_router, tags=["TestCase"])

__all__ = ["router"]
