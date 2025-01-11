import os

from pydantic_settings import BaseSettings
from dynaconf import Dynaconf


def config_file(f):
    return os.path.join("configs", f)


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[config_file(f"config-dev.toml")],
)


class Config(BaseSettings):
    APP_HOST: str = settings.project.app_host
    APP_PORT: int = settings.project.port
    RUN_SCHEDULER: bool = settings.project.run_scheduler
    DB_URL: str = os.getenv("TEST_GENIE_DB_URL")
    DEFAULT_PASSWORD: str = os.getenv("TEST_GENIE_DEFAULT_PASSWORD")
    OPENAI_API_KEY: str = os.getenv("TEST_GENIE_OPENAI_API_KEY")
    SHOULD_CREATE_TABLES: bool = settings.db.should_create_tables
    LOG_LEVEL: str = settings.log.level


def get_config():
    return Config()


config: Config = get_config()
