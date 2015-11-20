from __future__ import with_statement
from alembic import context
from sqlalchemy import create_engine, pool
from logging.config import dictConfig

import sys
import os.path

# Add the directory above the migrations dir to the path to ensure all the
# models can be found.
sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir)))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set up the loggers. This is essentially the loggers from the default config
# in dict form.
dictConfig({
    'version': 1,
    'root': {
        'level': 'WARN',
        'handlers': ['console']
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'level': 'NOTSET',
            'formatter': 'generic',
        },
    },
    'formatters': {
        'generic': {
            'format': '%(levelname)-5.5s [%(name)s] %(message)s',
            'datefmt': '%H:%M:%S',
        }
    },
    'loggers': {
        'alembic': {
            'level': 'INFO',
            'handlers': [],
        },
        'sqlalchemy': {
            'level': 'WARN',
            'handlers': ['console'],
        },
    },
})

# target_metadata is used for autogenerate support
from seabird.db import Base
target_metadata = Base.metadata

# Get the config module
# TODO: Make sure the default is only in one place.
import config
db_uri = config.args.get('db_uri', 'sqlite:///seabird.db')

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=db_uri, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = create_engine(db_uri)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
