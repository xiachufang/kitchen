import datetime
from peewee import DateTimeField
from .base import BaseDAO
from kitchen.libs.fields import UnsignedBigIntegerField


class UserDAO(BaseDAO):
    user_id = UnsignedBigIntegerField(null=False, index=True)
    recipe_id = UnsignedBigIntegerField(null=False)
    sequence = DateTimeField(default=datetime.datetime.now, null=False)


class RecipeDAO(BaseDAO):
    recipe_id = UnsignedBigIntegerField(null=False, index=True)
    user_id = UnsignedBigIntegerField(null=False)
    sequence = DateTimeField(default=datetime.datetime.now, null=False)
