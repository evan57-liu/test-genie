from openai import OpenAI

from test_genie.core.configs import config
from test_genie.core.db.database import Database
from test_genie.app.models import Base
from test_genie.app.service import (
    FileService,
    UserService,
    TestCaseService,
)


class Container:
    db = Database(config.DB_URL)
    if config.SHOULD_CREATE_TABLES:
        Base.metadata.create_all(db.sync_engine)

    openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

    file_service = FileService(session_factory=db.session)
    user_service = UserService(session_factory=db.session)
    testcase_service = TestCaseService(session_factory=db.session, openai_client=openai_client)
