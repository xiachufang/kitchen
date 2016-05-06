from bottle import request
from kitchen.app import app
from kitchen.models.collect import CollectRecipe


@app.route('/recipes/collected_by_user')
def recipes_collected_by_user():
    user_id = int(request.query.get('user_id'))
    cursor = int(request.query.get('cursor', '0'))
    size = int(request.query.get('size', 20))
    recipe_ids = CollectRecipe.targets_by_user(user_id, cursor, size)
    return {
        'recipe_ids': recipe_ids
    }

from peewee import Model, IntegerField, DateTimeField
from playhouse.db_url import connect

db = connect('mysql+pool://kitchen:@172.31.1.229:3306/original', max_connections=200)


class Collect(Model):
    class Meta:
        database = db

    user_id = IntegerField(null=False)
    recipe_id = IntegerField(null=False)
    create_time = DateTimeField(null=False)


@app.route('/recipes/collected_by_user2')
def recipes_collected_by_user2():
    db.connect()
    user_id = int(request.query.get('user_id'))
    recipe_ids = [c for c, in Collect.select(Collect.recipe_id).where(
        Collect.user_id == user_id
    ).order_by(Collect.id.desc()).limit(20).tuples()]
    recipe_ids = [c for c, in Collect.select(Collect.recipe_id).where(
        Collect.user_id == user_id
    ).order_by(Collect.id.desc()).limit(20).tuples()]
    recipe_ids = [c for c, in Collect.select(Collect.recipe_id).where(
        Collect.user_id == user_id
    ).order_by(Collect.id.desc()).limit(20).tuples()]
    recipe_ids = [c for c, in Collect.select(Collect.recipe_id).where(
        Collect.user_id == user_id
    ).order_by(Collect.id.desc()).limit(20).tuples()]
    db.close()
    return {
        'recipe_ids': recipe_ids
    }
