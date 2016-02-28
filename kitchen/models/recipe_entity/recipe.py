import datetime
import sqlalchemy as sa
from kitchen.libs.sqlalchemy_json_type import JSONType
from kitchen.models.base import metadata, ObjectBaseModel


class Recipe(ObjectBaseModel):
    type_id = 2
    table = sa.Table('recipe', metadata,
        sa.Column('local_id', sa.Integer, primary_key=True, autoincrement=True,
            nullable=False),
        sa.Column('data', JSONType, nullable=False, default='{}'),
        sa.Column('sequence', sa.DateTime(timezone=True), nullable=False,
            default=datetime.datetime.now)
    )

    def __repr__(self):
        return '<Recipe:{shard_id}:{local_id} {id} {name}>'.format(
            id=self.id, shard_id=self.shard_id, local_id=self.local_id,
            name=self.data['name'])

    @classmethod
    def create(cls, name, author, cover, ings, steps, desc='', tip=''):
        '''
        Args:
            name (str): Recipe name.
            author (User): Author of the recipe.
            cover (str): Ident of the recipe cover.
            ings (list): List of ingredients.

                [{'text': 'name of ing', 'unit': 'unit'},
                 {'text': 'name of ing', 'unit': 'unit'}]

            steps (list): List of steps.

                [{'text': 'name of step', 'image': 'ident'},
                 {'text': 'name of step', 'image': 'ident'},]

            desc (str): Description of the recipe.
            tip (str): Tips

        Returns:
            Recipe object
        '''
        data = {
            'name': name,
            'desc': desc,
            'author': {
                'id': author.id,
            },
            'cover': cover,
            'ings': ings,
            'steps': steps,
            'tip': tip,
        }

        return super(Recipe, cls).create(data=data)

    @classmethod
    def update(cls, id, name, cover, ings, steps, desc, tip):
        '''
        Args:
            id (int): Recipe ID
            name (str): Recipe name.
            cover (str): Ident of the recipe cover.
            ings (list): List of ingredients.

                [{'text': 'name of ing', 'unit': 'unit'},
                 {'text': 'name of ing', 'unit': 'unit'}]

            steps (list): List of steps.

                [{'text': 'name of step', 'image': 'ident'},
                 {'text': 'name of step', 'image': 'ident'},]

            desc (str): Description of the recipe.
            tip (str): Tips

        Returns:
            Recipe object
        '''
        engine = cls.get_engine(id)
        with engine.begin():
            r = cls.get(id, for_update=True)
            data = {
                'name': name,
                'desc': desc,
                'author': {
                    'id': r.data.author.id,
                },
                'cover': cover,
                'ings': ings,
                'steps': steps,
                'tip': tip,
            }
            return super(Recipe, cls).update(id, data=data)
