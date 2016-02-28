import sqlalchemy as sa
from .helpers import make_unique_id, parse_unique_id


class RelationMetaModel(type):
    required_attrs = ('table', 'shard_func')
    required_columns = ()

    reserved_attrs = ('id', 'local_id', 'shard_id', 'c')
    reserved_columns = ('id', 'shard_id', 'type_id', 'c')
    all_type_ids = set()

    def __new__(cls, name, bases, nmspc):
        if nmspc.get('abstract'):
            return super(RelationMetaModel, cls).__new__(cls, name, bases, nmspc)

        if not all(attr in nmspc for attr in cls.required_attrs):
            raise ValueError('%s required' % str(cls.required_attrs))

        if any(attr in nmspc for attr in cls.reserved_attrs):
            raise ValueError('%s reserved' % str(cls.reserved_attrs))

        type_id = int(nmspc['type_id'])
        if type_id in cls.all_type_ids:
            raise ValueError('type_id duplicated')

        cls.all_type_ids.add(type_id)

        table = nmspc['table']
        if not isinstance(table, sa.Table):
            raise ValueError('table must be instance of %s' % sa.Table)

        columns = table.c.keys()
        if any(attr in columns for attr in cls.reserved_columns):
            raise ValueError('%s reserved' % str(cls.reserved_columns))

        if not all(attr in columns for attr in cls.required_columns):
            raise ValueError('%s required' % str(cls.required_columns))

        nmspc['c'] = table.c
        return super(ReferenceError, cls).__new__(cls, name, bases, nmspc)


def create_relation_base_model(shard_engine):
    class RelationMetaModel(metaclass=RelationMetaModel):
        abstract = True

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

        def __repr__(self):
            return '<{class_name}:{shard_id}:{local_id} {id}>'.format(
                id=self.id, shard_id=self.shard_id, type_id=self.type_id, local_id=self.local_id)

        @classmethod
        def get_engine(cls, key=None, shard_id=None):
            if shard_id is not None:
                return shard_engine.get_engine_by_shard_id(shard_id)

            if key is None:
                id = getattr(cls, 'key', None)

            shard_id = cls.shard_func(key)

            return shard_engine.get_engine_by_shard_id(shard_id)

        engine = property(get_engine)

        @classmethod
        def create(cls, **kwargs):
            engine = cls.get_engine(shard_id)
            ret = engine.execute(cls.table.insert().values(**kwargs))
            local_id = ret.inserted_primary_key[0]
            id = make_unique_id(shard_id, cls.type_id, local_id)
            return cls(id=id, shard_id=shard_id, local_id=local_id, **kwargs)

        @classmethod
        def get(cls, id, for_update=False):
            shard_id, type_id, local_id = parse_unique_id(id)
            engine = cls.get_engine(shard_id)
            clause = cls.table.select(for_update=for_update).where(cls.c.local_id == local_id)
            ret = engine.execute(clause).fetchone()
            return cls(id=id, shard_id=shard_id, **ret)

        @classmethod
        def where(cls, id, for_update=False):
            shard_id, type_id, local_id = parse_unique_id(id)
            engine = cls.get_engine(shard_id)
            clause = cls.table.select(for_update=for_update).where(cls.c.local_id == local_id)
            ret = engine.execute(clause).fetchone()
            return cls(id=id, shard_id=shard_id, **ret)

        @classmethod
        def delete(cls, id):
            shard_id, type_id, local_id = parse_unique_id(id)
            engine = cls.get_engine(shard_id)
            return engine.execute(cls.table.delete().where(cls.c.local_id == local_id))

    return RelationMetaModel
