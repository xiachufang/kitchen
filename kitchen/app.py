from bottle import Bottle
from kitchen.daos.base import shard_db
from kitchen.settings.db_settings import shard_settings


app = Bottle()

shard_db.configure(shard_settings)


@app.hook('before_request')
def _connect_db():
    shard_db.connect()


@app.hook('after_request')
def _close_db():
    shard_db.close()


import kitchen.views.collect
