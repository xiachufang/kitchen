from peewee import Model, IntegerField, DateTimeField
from playhouse.db_url import connect
from kitchen.models.collect import CollectRecipe
from kitchen.settings.db_settings import shard_settings
from kitchen.daos.base import shard_db

shard_db.configure(shard_settings)


db = connect('mysql+pool://kitchen:@172.31.1.229:3306/original', max_connections=200)


class Collect(Model):
    class Meta:
        database = db

    user_id = IntegerField(null=False)
    recipe_id = IntegerField(null=False)
    create_time = DateTimeField(null=False)


def ormiter(orm, where=[], limit=1000):
    id = 0
    while True:
        if where:
            r = orm.select().where(*where)
        else:
            r = orm.select()
        total = list(r.where(orm.id > id).limit(limit))
        if total:
            for i in total:
                yield i
            id = total[-1].id
        else:
            break

for c in ormiter(Collect):
    print c.id
    CollectRecipe.insert(c.user_id, c.recipe_id, c.create_time)
