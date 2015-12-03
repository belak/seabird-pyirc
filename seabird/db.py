from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, IntegrityError
from sqlalchemy.orm.session import Session

from PyIRC.extensions import BaseExtension

from contextlib import contextmanager

# This should be the base for all models in seabird, so migrations can be
# auto-generated.
Base = declarative_base()  # pylint:disable=invalid-name


class SeabirdSession(Session):
    def get_or_create(self, model, **kwargs):
        # http://stackoverflow.com/a/21146492
        try:
            return self.query(model).filter_by(**kwargs).one(), True
        except NoResultFound:
            created = model(**kwargs)
            try:
                self.add(created)
                self.flush()
                return created, False
            except IntegrityError:
                self.rollback()
                return self.query(model).filter_by(**kwargs).one(), True


class Database(BaseExtension):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.db_engine = create_engine(kwargs.pop('db_uri',
                                                  'sqlite:///bot.db'))
        self.db_sessionmaker = sessionmaker(bind=self.db_engine,
                                            class_=SeabirdSession)

        # Monkey patch the db_session method onto the bot object because people
        # are lazy.
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
