from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import declarative_base

from test_genie.core.db.timestamp_mixin import TimestampMixin
from test_genie.app.enums import PromptType, TestCaseStatus

Base = declarative_base()


@dataclass
class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)


@dataclass
class File(Base, TimestampMixin):
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    path: Mapped[str] = mapped_column(String(256), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)


@dataclass
class Prompt(Base, TimestampMixin):
    __tablename__ = "prompt"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[PromptType] = mapped_column(Enum(PromptType), nullable=False)
    file_id: Mapped[int] = mapped_column(Integer, ForeignKey("file.id"), nullable=False)


@dataclass
class TestCase(Base, TimestampMixin):
    __tablename__ = "test_case"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    result: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[TestCaseStatus] = mapped_column(Enum(TestCaseStatus), nullable=False)
    file_id: Mapped[int] = mapped_column(Integer, ForeignKey("file.id"), nullable=False)

    file: Mapped["File"] = relationship("File", lazy=False)
