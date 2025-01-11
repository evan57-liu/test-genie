from enum import Enum


class PromptType(Enum):
    DEFAULT = "DEFAULT"
    CUSTOM = "CUSTOM"


class TestCaseStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"