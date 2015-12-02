from sqlalchemy import MetaData
from kitchen.libs.shard import ShardEngine, create_object_base_model
from kitchen.settings import db_settings

shard_engine = ShardEngine(db_settings.shard_settings, echo=False)
metadata = MetaData()
ObjectBaseModel = create_object_base_model(shard_engine)
