from sqlalchemy import event
from sqlalchemy.engine import Engine
from .connection import ShardConnection


class ShardEngine:
    def __init__(self, hosts, **db_config):
        '''
        settings:
            [
                {'range': range(0, 511), 'master': 'MySQL001A', 'slave': 'MySQL001B'},
                {'range': range(512, 1023), 'master': 'MySQL002A', 'slave': 'MySQL002B'},
                {'range': range(3584, 4095), 'master': 'MySQL008A', 'slave': 'MySQL008B'}
            ]
        '''
        self.shard_connection = ShardConnection(hosts, **db_config)

        @event.listens_for(Engine, "before_cursor_execute")
        def _switch_shard(conn, cursor, stmt, params, context, executemany):
            shard_id = conn._execution_options.get('shard_id', None)
            if shard_id is None:
                return
            current_shard = conn.info.get("current_shard")

            if current_shard != shard_id:
                cursor.execute("use %s" % self.get_db_name_by_shard_id(shard_id))
                conn.info["current_shard"] = shard_id

    @property
    def shard_ids(self):
        return self.shard_connection.shard_ids

    def get_db_name_by_shard_id(self, shard_id):
        return self.shard_connection.get_db_name_by_shard_id(shard_id)

    def get_host_by_shard_id(self, shard_id):
        return self.shard_connection.get_host_by_shard_id(shard_id)

    def get_connection_by_shard_id(self, shard_id):
        return self.shard_connection.get_connection_by_shard_id(shard_id)

    def get_engine_by_shard_id(self, shard_id):
        conn = self.get_connection_by_shard_id(shard_id)
        if conn._execution_options.get('shard_id') != shard_id:
            conn.update_execution_options(shard_id=shard_id)
        return conn


def create_databases_and_tables(shard_engine, metadata):
    for shard_id in shard_engine.shard_ids:
        db_name = shard_engine.get_db_name_by_shard_id(shard_id)
        conn = shard_engine.get_connection_by_shard_id(shard_id)
        conn.execute('CREATE DATABASE IF NOT EXISTS %s' % db_name)

        engine = shard_engine.get_engine_by_shard_id(shard_id)
        metadata.create_all(engine)


def drop_databases(shard_engine):
    for shard_id in shard_engine.shard_ids:
        db_name = shard_engine.get_db_name_by_shard_id(shard_id)
        conn = shard_engine.get_connection_by_shard_id(shard_id)
        conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
