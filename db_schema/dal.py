from contextlib import contextmanager
import logging
import os


from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

logger = logging.getLogger(__name__)


class DAL:
    """Data access layer."""

    def __init__(self, uri, user, password, db_name):
        self.db_uri = uri
        self.db_user = user
        self.db_password = password
        self.db_name = db_name

        self._engine = None
        self._sessionmaker = None

    @classmethod
    def from_env(cls):
        return cls(
            uri=os.environ["DB_URI"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            db_name=os.environ["POSTGRES_DB"],
        )

    @property
    def engine(self):
        if self._engine is None:
            logger.debug(f"creating an engine towards {self.db_uri}")
            self._engine = create_engine(
                "postgresql+psycopg2://"
                f"{self.db_user}:{self.db_password}@{self.db_uri}/{self.db_name}"
            )
        return self._engine

    @property
    def sessionmaker(self):
        if self._sessionmaker is None:
            self._sessionmaker = sessionmaker(bind=self.engine)
        return self._sessionmaker

    def get_session(self):
        return self.sessionmaker()

    @contextmanager
    def session_scope(self):
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.error("An error occurred in session scope, rollbacking...")
            session.rollback()
            raise e
        finally:
            session.close()
