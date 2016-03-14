import hashlib
from playhouse.pool import PooledMySQLDatabase
from .config import ShardConfig


class PooledMySQLMutipleDatabase(PooledMySQLDatabase):
    def __init__(self, *args, **kwargs):
        super(PooledMySQLMutipleDatabase, self).__init__(database='', *args, **kwargs)

    def use_db(self, db_name):
        self.execute_sql('USE %s' % db_name)


class ShardDatabase(object):
    def configure(self, conf):
        '''
        config: Config object
        '''
        self.connections = {}
        self.selected_db = {}
        self.config = ShardConfig(conf)
        for host_conf in self.config.hosts:
            host_url = host_conf['master']
            db = PooledMySQLMutipleDatabase(
                host=host_url,
                user=self.config.username,
                password=self.config.password
            )
            self.connections[host_url] = db
            self.selected_db[host_url] = None
        self.current_db = None

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
        if self.selected_db[host_url] != db_name:
            conn.use_db(db_name)
            self.selected_db[host_url] = db_name
        return conn

    def select_shard_by_shard_id(self, shard_id):
        self.current_db = self.get_db_by_shard_id(shard_id)
        return self

    def select_shard(self, key):
        k = str(key)
        if isinstance(k, str):
            k = k.encode('utf-8')
        shard_id = int(hashlib.md5(k).hexdigest(), 16) % self.config.total_shards
        self.select_shard_by_shard_id(shard_id)
        return self

    def __getattr__(self, k, v=None):
        if not self.current_db:
            raise ValueError('no current db')
        return getattr(self.current_db, k, v)


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
        shard_db.execute_sql('DROP DATABASE IF EXISTS `%s`;' % db_name)
