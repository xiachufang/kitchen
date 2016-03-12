import logging
import pytest
from kitchen.daos.base import shard_db
from kitchen.libs.shard.engine import create_databases_and_tables, drop_databases
from kitchen import daos
from kitchen.settings.db_settings import shard_settings


# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

shard_db.configure(shard_settings)


@pytest.yield_fixture(autouse=True)
def db():
    tables = []
    for k in dir(daos):
        if k.endswith('DAO'):
            dao_cls = getattr(daos, k)
            if issubclass(dao_cls, daos.base.BaseDAO):
                tables.append(dao_cls)

    create_databases_and_tables(shard_db, tables)
    try:
        yield
    finally:
        drop_databases(shard_db)
