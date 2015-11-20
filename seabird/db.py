from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from PyIRC.extensions import BaseExtension

from contextlib import contextmanager

# This should be the base for all models in seabird, so migrations can be
# auto-generated.
Base = declarative_base()


class Database(BaseExtension):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.db_engine = create_engine(kwargs.pop('db_uri', 'sqlite:///seabird.db'))
        self.db_sessionmaker = sessionmaker(bind=self.db_engine)

        # Monkey patch the db_session method onto the bot object because people are lazy.
        self.base.db_session = self.db_session

    @contextmanager
    def db_session(self):
        """Provide a transactional scope around a series of operations.

        This is taken from the SQLAlchemy docs and adapted slightly to fit in
        here.

        It will be available on the bot object as db_session.
        """
        session = self.db_sessionmaker()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
