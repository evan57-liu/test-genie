import logging
from contextlib import contextmanager

from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self.sync_engine = create_engine(
            db_url,
            pool_pre_ping=True,
            echo=True
        )
        self.sync_session_factory = sessionmaker(
            self.sync_engine,
            expire_on_commit=False,
            autoflush=False,
            future=True,
        )

    @contextmanager
    def session(self) -> Session:
        # session transactions are started by default
        # if you want several sql statements in the same transaction, pass the fetched session
        session = self.sync_session_factory()
        try:
            # the role here is to provide autocommit and auto rollback,
            # if you have exception here, it will be rollback and raise the exception
            with session.begin():
                yield session
        except Exception as e:
            logger.error('Session rollback because of exception: %s', e)
            raise e
        finally:
            session.close()
