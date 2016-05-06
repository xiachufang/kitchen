import threading
import hashlib
from playhouse.pool import PooledMySQLDatabase
from .config import ShardConfig


class PooledMySQLMutipleDatabase(PooledMySQLDatabase):
    def __init__(self, *args, **kwargs):
        super(PooledMySQLMutipleDatabase, self).__init__(database='', *args, **kwargs)

    def use_db(self, db_name):
        self.execute_sql('USE %s' % db_name)


class ShardDatabase(object):
    def __init__(self):
        self.connections = {}
        self.config = None
        self.local = threading.local()
        self.local.selected_catalog = {}
        self.local.current_db = None

    def configure(self, conf):
        '''
        config: Config object
        '''
        self.config = ShardConfig(conf)
        for host_conf in self.config.hosts:
            host_url = host_conf['master']
            conn = PooledMySQLMutipleDatabase(
                host=host_url,
                user=self.config.username,
                password=self.config.password
            )
            self.connections[host_url] = conn
            self.local.selected_catalog[host_url] = None

    def __iter__(self):
        for shard_id in self.config.shard_ids:
            yield self.get_db_by_shard_id(shard_id)

    def get_conn_by_shard_id(self, shard_id):
        host_conf = self.config.get_host_by_shard_id(shard_id)
        host_url = host_conf['master']
        return self.connections[host_url]

    def get_db_by_shard_id(self, shard_id):
        host_conf = self.config.get_host_by_shard_id(shard_id)
        host_url = host_conf['master']
        db_name = self.config.get_db_name_by_shard_id(shard_id)
        conn = self.connections[host_url]
        if self.local.selected_catalog[host_url] != db_name:
            conn.use_db(db_name)
            self.local.selected_catalog[host_url] = db_name
        return conn

    def select_shard_by_shard_id(self, shard_id):
        self.local.current_db = self.get_db_by_shard_id(shard_id)
        return self

    def select_shard(self, key):
        k = str(key)
        if isinstance(k, str):
            k = k.encode('utf-8')
        shard_id = int(hashlib.md5(k).hexdigest(), 16) % self.config.total_shards
        self.select_shard_by_shard_id(shard_id)
        return self

    def connect(self):
        for conn in self.connections.values():
            conn.connect()

    def close(self):
        for conn in self.connections.values():
            conn.close()

    def __getattr__(self, k, v=None):
        if not self.local.current_db:
            raise ValueError('no current db')
        return getattr(self.local.current_db, k, v)


def create_databases_and_tables(shard_db, models):
    for shard_id in shard_db.config.shard_ids:
        db_name = shard_db.config.get_db_name_by_shard_id(shard_id)
        conn = shard_db.get_conn_by_shard_id(shard_id)
        conn.execute_sql('CREATE DATABASE IF NOT EXISTS %s;' % (db_name,))
        shard_db.select_shard_by_shard_id(shard_id)
        shard_db.create_tables(models, safe=True)


def drop_databases(shard_db):
    for shard_id in shard_db.config.shard_ids:
        db_name = shard_db.config.get_db_name_by_shard_id(shard_id)
        shard_db.select_shard_by_shard_id(shard_id)
        sql = 'DROP DATABASE IF EXISTS `%s`;' % db_name
        shard_db.execute_sql(sql)
