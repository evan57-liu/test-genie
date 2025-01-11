from functools import wraps

from sqlalchemy.orm import scoped_session


class Transactional:

    def __init__(self, session_factory: scoped_session):
        self.session_factory = session_factory

    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            with self.session_factory() as s, s.begin():
                return func(s, *args, **kwargs)

        return _transactional
