import sqlalchemy as sa
from sqlalchemy.sql import and_
from kitchen.models.base import metadata
from ..base import shard_engine


recipes_collected_by_user = sa.Table(
    'recipes_collected_by_user',
    metadata,
    sa.Column('local_id', sa.Integer, primary_key=True, autoincrement=True,
              nullable=False),
    sa.Column('user_id', sa.Integer, nullable=False, index=True),
    sa.Column('recipe_id', sa.Integer, nullable=False),
    sa.Column('sequence', sa.DateTime(timezone=True), nullable=False)
)

users_collecting_recipe = sa.Table(
    'users_collecting_recipe',
    metadata,
    sa.Column('local_id', sa.Integer, primary_key=True, autoincrement=True,
              nullable=False),
    sa.Column('user_id', sa.Integer, nullable=False),
    sa.Column('recipe_id', sa.Integer, nullable=False, index=True),
    sa.Column('sequence', sa.DateTime(timezone=True), nullable=False)
)


def shard_func(key):
    ret = hash(key) % len(shard_engine.shard_ids)
    return ret


def user_shard(key):
    return shard_engine.get_engine_by_shard_id(shard_func(key))

recipe_shard = user_shard


class Collect:

    @classmethod
    def create(cls, user_id, recipe_id, sequence):
        user_shard(user_id).execute(recipes_collected_by_user.insert().values(user_id=user_id, recipe_id=recipe_id, sequence=sequence))
        recipe_shard(recipe_id).execute(users_collecting_recipe.insert().values(user_id=user_id, recipe_id=recipe_id, sequence=sequence))

    @classmethod
    def delete(cls, user_id, recipe_id):
        clause = recipes_collected_by_user.delete().where(and_(
            recipes_collected_by_user.c.user_id == user_id,
            recipes_collected_by_user.c.recipe_id == recipe_id
        ))
        user_shard(user_id).execute(clause)
        clause = users_collecting_recipe.delete().where(and_(
            users_collecting_recipe.c.user_id == user_id,
            users_collecting_recipe.c.recipe_id == recipe_id
        ))
        recipe_shard(recipe_id).execute(clause)

    @classmethod
    def recipes_collected_by_user(cls, user_id, cursor=0, size=20):
        user_shard(user_id).execute(recipes_collected_by_user.select().where(
            recipes_collected_by_user.c.user_id == user_id
        ).limit(size).offset(cursor))

    @classmethod
    def users_collecting_recipe(cls, recipe_id, cursor=0, size=20):
        recipe_shard(recipe_id).execute(users_collecting_recipe.select().where(
            users_collecting_recipe.c.recipe_id == recipe_id
        ).limit(size).offset(cursor))
