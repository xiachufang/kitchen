from unittest.mock import MagicMock # noqa
from kitchen.models.recipe import Recipe, shard_engine, metadata # noqa
from kitchen.libs.shard import create_databases_and_tables, drop_databases # noqa


# drop_databases(shard_engine)
# create_databases_and_tables(shard_engine, metadata)

r = Recipe.create(name='红烧肉', author=MagicMock(id=1), cover='ident_cover',
    ings=[{'text': '水', 'unit': '很多'}, {'text': '肉'}, {'text': '葱花'}],
    steps=[{'text': '焯水', 'ident': 'i1'}, {'text': '爆炒', 'ident': ''}, {'text': '收汁'}],
    desc='很好吃很家常的红烧肉', tip='')

# print(type(r.data))

# print(r, r.data.name)

Recipe.update(r.id, name='懒人红烧肉', cover='ident_cover',
    ings=[{'text': '水', 'unit': '很多'}, {'text': '肉'}, {'text': '葱花'}],
    steps=[{'text': '焯水', 'ident': 'i1'}, {'text': '爆炒', 'ident': ''}, {'text': '收汁'}],
    desc='很好吃很家常的红烧肉', tip='')

r = Recipe.get(r.id)
print(r.data)
print('get', r, r.data.name)

