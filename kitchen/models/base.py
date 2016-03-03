import random
from sqlalchemy import MetaData
from kitchen.libs.shard import ShardEngine, create_object_base_model
from kitchen.settings import db_settings

shard_engine = ShardEngine(db_settings.shard_settings, echo=False)
metadata = MetaData()


def choose_shard_id():
    shard_id = random.choice(shard_engine.shard_ids)
    return shard_id


class ObjectBaseModel(create_object_base_model(shard_engine)):
    abstract = True
    shard_func = choose_shard_id
