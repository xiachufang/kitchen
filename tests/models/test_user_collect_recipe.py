import pytest
import datetime
from kitchen.models.collect import Collect, UserDAO, RecipeDAO


@pytest.fixture(params=range(4))
def user_id(request):
    return request.param


@pytest.fixture(params=range(4))
def recipe_id(request):
    return request.param


class TestCollect:
    def test_create(self, user_id, recipe_id):
        sequence = datetime.datetime.now()

        Collect.insert(user_id, recipe_id, sequence)

        assert UserDAO.select_shard(user_id).select().where(
            UserDAO.user_id == user_id,
            UserDAO.recipe_id == recipe_id,
        ).count() == 1
        assert RecipeDAO.select_shard(recipe_id).select().where(
            RecipeDAO.user_id == user_id,
            RecipeDAO.recipe_id == recipe_id,
        ).count() == 1

    def test_delete(self, user_id, recipe_id):
        sequence = datetime.datetime.now()

        Collect.insert(user_id, recipe_id, sequence)

        Collect.delete(user_id, recipe_id)

        assert UserDAO.select_shard(user_id).select().where(
            UserDAO.user_id == user_id,
            UserDAO.recipe_id == recipe_id,
        ).count() == 0
        assert RecipeDAO.select_shard(recipe_id).select().where(
            RecipeDAO.user_id == user_id,
            RecipeDAO.recipe_id == recipe_id,
        ).count() == 0

    def test_recipes_collected_by_user(self, recipe_id, user_id):
        Collect.insert(user_id, recipe_id)
        assert Collect.recipes_collected_by_user(user_id) == [recipe_id]
        Collect.delete(user_id, recipe_id)
        assert Collect.recipes_collected_by_user(user_id) == []

    def test_users_collecting_recipe(self, recipe_id, user_id):
        Collect.insert(user_id, recipe_id)
        assert Collect.users_collecting_recipe(recipe_id) == [user_id]
        Collect.delete(user_id, recipe_id)
        assert Collect.users_collecting_recipe(recipe_id) == []

    def test_count_recipes_collected_by_user(self, recipe_id, user_id):
        Collect.insert(user_id, recipe_id)
        assert Collect.recipes_collected_by_user(user_id) == 1
        Collect.delete(user_id, recipe_id)
        assert Collect.recipes_collected_by_user(user_id) == 0

    def test_count_recipe_collected_times(self, recipe_id, user_id):
        Collect.insert(user_id, recipe_id)
        assert Collect.count_recipe_collected_times(recipe_id) == 1
        Collect.delete(user_id, recipe_id)
        assert Collect.count_recipe_collected_times(recipe_id) == 0
