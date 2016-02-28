import datetime
import sqlalchemy as sa

table = sa.Table('recipe', metadata,
                 sa.Column('local_id', sa.Integer, primary_key=True, autoincrement=True,
                           nullable=False),
                 sa.Column('data', JSONType, nullable=False, default='{}'),
                 sa.Column('sequence', sa.DateTime(timezone=True), nullable=False,
                           default=datetime.datetime.now)
                 )
