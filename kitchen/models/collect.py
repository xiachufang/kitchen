import datetime
from kitchen.daos.collect import UserDAO, RecipeDAO


class Collect(object):
    @classmethod
    def insert(cls, user_id, recipe_id, sequence=None):
        if not sequence:
            sequence = datetime.datetime.now()
        UserDAO.select_shard(user_id).insert(user_id=user_id, recipe_id=recipe_id, sequence=sequence).execute()
        RecipeDAO.select_shard(recipe_id).insert(user_id=user_id, recipe_id=recipe_id, sequence=sequence).execute()

    @classmethod
    def delete(cls, user_id, recipe_id):
        UserDAO.select_shard(user_id).delete().where(
            UserDAO.user_id == user_id,
            UserDAO.recipe_id == recipe_id
        ).execute()
        RecipeDAO.select_shard(recipe_id).delete().where(
            RecipeDAO.user_id == user_id,
            RecipeDAO.recipe_id == recipe_id
        ).execute()

    @classmethod
    def recipes_collected_by_user(cls, user_id, cursor=0, size=20):
        return UserDAO.select_shard(user_id).select(UserDAO.recipe_id).where(
            UserDAO.user_id == user_id
        ).order_by(UserDAO.sequence.desc()).limit(size).offset(cursor)

    @classmethod
    def users_collecting_recipe(cls, recipe_id, cursor=0, size=20):
        return RecipeDAO.select_shard(recipe_id).select(RecipeDAO.recipe_id).where(
            RecipeDAO.recipe_id == recipe_id
        ).order_by(RecipeDAO.sequence.desc()).limit(size).offset(cursor)

    @classmethod
    def count_recipes_collected_by_user(cls, user_id):
        return UserDAO.select_shard(user_id).select().where(
            UserDAO.user_id == user_id
        ).count()

    @classmethod
    def count_recipe_collected_times(cls, recipe_id):
        return RecipeDAO.select_shard(recipe_id).select().where(
            RecipeDAO.recipe_id == recipe_id
        ).count()

    @classmethod
    def if_recipes_are_collected_by_user(cls, recipe_ids, user_id):
        collected_recipe_ids = UserDAO.select_shard(user_id).select(UserDAO.recipe_id).where(
            UserDAO.user_id._in(recipe_ids)
        ).execute()
        return dict((str(rid), int(rid) in collected_recipe_ids) for rid in recipe_ids)
