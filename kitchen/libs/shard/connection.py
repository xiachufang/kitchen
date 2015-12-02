from sqlalchemy import create_engine
from .config import ShardConfig


class ShardConnection:
    def __init__(self, hosts, **db_config):
        '''
        settings:
            [
                {'range': range(0, 511), 'master': 'MySQL001A', 'slave': 'MySQL001B'},
                {'range': range(512, 1023), 'master': 'MySQL002A', 'slave': 'MySQL002B'},
                {'range': range(3584, 4095), 'master': 'MySQL008A', 'slave': 'MySQL008B'}
            ]
        '''
        self.config = ShardConfig(hosts, **db_config)
        self.connections = {}

    @property
    def shard_ids(self):
        return self.config.shard_ids

    def get_db_name_by_shard_id(self, shard_id):
        return self.config.get_db_name_by_shard_id(shard_id)

    def get_host_by_shard_id(self, shard_id):
        return self.config.get_host_by_shard_id(shard_id)

    def get_connection_by_shard_id(self, shard_id):
        urls = self.get_host_by_shard_id(shard_id)
        master_url = urls['master'].strip()
        conn = self.connections.get(master_url)
        if not conn:
            conn = create_engine(urls['master'], **self.config.db_config)
            self.connections['master_url'] = conn

        return conn
