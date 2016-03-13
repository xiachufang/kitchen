import logging
import pytest
from kitchen.daos.base import shard_db, BaseDAO
from kitchen.libs.shard.engine import create_databases_and_tables, drop_databases
from kitchen.settings.db_settings import shard_settings


# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

shard_db.configure(shard_settings)


@pytest.yield_fixture(autouse=True)
def db():
    create_databases_and_tables(shard_db, BaseDAO.__class__.models)
    try:
        yield
    finally:
        drop_databases(shard_db)
