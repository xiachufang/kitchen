from kitchen.models.base import shard_engine, metadata
from kitchen.libs.shard import create_databases_and_tables, drop_databases # noqa


import kitchen.models.recipe # noqa


drop_databases(shard_engine)
create_databases_and_tables(shard_engine, metadata)
