import datetime
import sqlalchemy as sa
from kitchen.libs.sqlalchemy_json_type import JSONType
from kitchen.models.base import metadata, ObjectBaseModel


class User(ObjectBaseModel):
    type_id = 1
    table = sa.Table('user', metadata,
        sa.Column('local_id', sa.Integer, primary_key=True, autoincrement=True,
            nullable=False),
        sa.Column('data', JSONType, nullable=False, default='{}'),
        sa.Column('sequence', sa.DateTime(timezone=True), nullable=False,
            default=datetime.datetime.now)
    )

    @classmethod
    def create(cls, name, desc=''):
        '''
        Args:
            name (str): Name.
            desc (str): Description of the recipe.

        Returns:
            User object
        '''
        data = {
            'name': name,
            'desc': desc,
        }

        return super(User, cls).create(data=data)

    @classmethod
    def update(cls, id, name, desc):
        '''
        Args:
            id (int): User ID
            name (str): User name.
            desc (str): Description of the user.

        Returns:
            User object
        '''
        engine = cls.get_engine(id)
        with engine.begin():
            data = {
                'name': name,
                'desc': desc,
            }
            return super(User, cls).update(id, data=data)
