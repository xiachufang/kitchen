import pytest
from kitchen.models.base import shard_engine, metadata
from kitchen.libs.shard import create_databases_and_tables, drop_databases


@pytest.yield_fixture(autouse=True)
def db():
    create_databases_and_tables(shard_engine, metadata)
    try:
        yield
    finally:
        drop_databases(shard_engine)
