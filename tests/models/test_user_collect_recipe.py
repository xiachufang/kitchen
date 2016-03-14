import pytest
import datetime
from kitchen.models.collect import CollectRecipe


@pytest.fixture(params=range(4))
def user_id(request):
    return request.param


@pytest.fixture(params=range(4))
def target_id(request):
    return request.param


UserDAO = CollectRecipe.UserDAO
RecipeDAO = CollectRecipe.TargetDAO


class TestCollectRecipe:
    def test_create(self, user_id, target_id):
        sequence = datetime.datetime.now()

        CollectRecipe.insert(user_id, target_id, sequence)

        assert UserDAO.select_shard(user_id).select().where(
            UserDAO.user_id == user_id,
            UserDAO.target_id == target_id,
        ).count() == 1
        assert RecipeDAO.select_shard(target_id).select().where(
            RecipeDAO.user_id == user_id,
            RecipeDAO.target_id == target_id,
        ).count() == 1

    def test_delete(self, user_id, target_id):
        sequence = datetime.datetime.now()

        CollectRecipe.insert(user_id, target_id, sequence)

        CollectRecipe.delete(user_id, target_id)

        assert UserDAO.select_shard(user_id).select().where(
            UserDAO.user_id == user_id,
            UserDAO.target_id == target_id,
        ).count() == 0
        assert RecipeDAO.select_shard(target_id).select().where(
            RecipeDAO.user_id == user_id,
            RecipeDAO.target_id == target_id,
        ).count() == 0

    def test_targets_by_user(self, target_id, user_id):
        CollectRecipe.insert(user_id, target_id)
        assert CollectRecipe.targets_by_user(user_id) == [target_id]
        CollectRecipe.delete(user_id, target_id)
        assert CollectRecipe.targets_by_user(user_id) == []

    def test_users_by_target(self, target_id, user_id):
        CollectRecipe.insert(user_id, target_id)
        assert CollectRecipe.users_by_target(target_id) == [user_id]
        CollectRecipe.delete(user_id, target_id)
        assert CollectRecipe.users_by_target(target_id) == []

    def test_count_targets_by_user(self, target_id, user_id):
        CollectRecipe.insert(user_id, target_id)
        assert CollectRecipe.targets_by_user(user_id) == 1
        CollectRecipe.delete(user_id, target_id)
        assert CollectRecipe.targets_by_user(user_id) == 0

    def test_count_users_by_target(self, target_id, user_id):
        CollectRecipe.insert(user_id, target_id)
        assert CollectRecipe.count_users_by_target(target_id) == 1
        CollectRecipe.delete(user_id, target_id)
        assert CollectRecipe.count_users_by_target(target_id) == 0
