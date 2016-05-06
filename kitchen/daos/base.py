from peewee import Model, SQL, DateTimeField
from kitchen.libs.shard.engine import ShardDatabase


shard_db = ShardDatabase()


class MetaClass(Model.__class__):
    models = set()

    def __new__(cls, name, bases, attrs):
        _meta = attrs.get('Meta', None)
        abstract = getattr(_meta, '_abstract', False) if _meta else False
        clazz = super(MetaClass, cls).__new__(cls, name, bases, attrs)
        if abstract:
            return clazz

        cls.models.add(clazz)
        return clazz


def with_metaclass(meta, base=object):
    class Meta:
        _abstract = True

    return meta('NewBase', (base,), {'Meta': Meta})


class BaseDAO(with_metaclass(MetaClass, Model)):
    class Meta:
        _abstract = True
        database = shard_db

    _create_time = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    _update_time = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')])

    @classmethod
    def select_shard(cls, key):
        shard_db.select_shard(key)
        return cls
