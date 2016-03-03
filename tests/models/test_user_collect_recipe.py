import pytest
import datetime
from sqlalchemy.sql import and_, func, select
from kitchen.models.recipe_entity.user_collect_recipe import (
    Collect, user_shard, recipe_shard, recipes_collected_by_user, users_collecting_recipe
)


@pytest.fixture(params=range(10))
def lot_user_id(request):
    return request.param


@pytest.fixture(params=range(10))
def lot_recipe_id(request):
    return request.param


class TestCollect:
    def test_create(self, lot_user_id, lot_recipe_id):
        user_id = lot_user_id
        recipe_id = lot_recipe_id
        sequence = datetime.datetime.now()

        Collect.create(user_id, recipe_id, sequence)

        clause = select([func.count(0)]).where(and_(
                users_collecting_recipe.c.user_id == user_id,
                users_collecting_recipe.c.recipe_id == recipe_id,
        ))
        assert recipe_shard(recipe_id).execute(clause).fetchone() == (1,)

        clause = select([func.count(0)]).where(and_(
                recipes_collected_by_user.c.user_id == user_id,
                recipes_collected_by_user.c.recipe_id == recipe_id,
        ))
        assert user_shard(user_id).execute(clause).fetchone() == (1,)

    def test_delete(self, lot_user_id, lot_recipe_id):
        user_id = lot_user_id
        recipe_id = lot_recipe_id
        sequence = datetime.datetime.now()

        Collect.create(user_id, recipe_id, sequence)

        Collect.delete(user_id, recipe_id)
        clause = select([func.count(0)]).where(and_(
                users_collecting_recipe.c.user_id == user_id,
                users_collecting_recipe.c.recipe_id == recipe_id,
        ))
        assert recipe_shard(recipe_id).execute(clause).fetchone() == (0,)

        clause = select([func.count(0)]).where(and_(
                recipes_collected_by_user.c.user_id == user_id,
                recipes_collected_by_user.c.recipe_id == recipe_id,
        ))
        assert user_shard(user_id).execute(clause).fetchone() == (0,)
