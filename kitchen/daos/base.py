from peewee import Model, SQL, DateTimeField
from kitchen.libs.shard.engine import ShardDatabase


shard_db = ShardDatabase()


class BaseDAO(Model):
    class Meta:
        database = shard_db

    @classmethod
    def select_shard(cls, key):
        shard_db.select_shard(key)
        return cls

    _create_time = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    _update_time = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')])
