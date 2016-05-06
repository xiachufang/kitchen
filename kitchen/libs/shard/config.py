import operator
from functools import reduce


class ShardConfig(object):
    def __init__(self, config):
        '''
        config:
        {
            'db_pattern': 'db%05d',
            'user': 'username',
            'password': 'xxx',
            'total_shards': 4096,
            'hosts': [
                {'range': range(0, 511), 'master': 'MySQL001A', 'slave': 'MySQL001B'},
                {'range': range(512, 1023), 'master': 'MySQL002A', 'slave': 'MySQL002B'},
                {'range': range(3584, 4095), 'master': 'MySQL008A', 'slave': 'MySQL008B'}
            ]
        }
        '''
        self.config = config
        db_config = config.copy()
        self.hosts = db_config.pop('hosts')
        self.username = db_config['user']
        self.password = db_config['password']
        self.db_pattern = db_config.pop('db_pattern', 'db%05d')
        self.db_config = db_config
        self.total_shards = int(config['total_shards'])
        self.shard_ids = reduce(operator.concat, map(operator.itemgetter('range'), self.hosts))

    def get_host_by_shard_id(self, shard_id):
        for s in self.hosts:
            if shard_id in s['range']:
                return s
        raise ValueError('no shard_id %s found' % shard_id)

    def get_db_name_by_shard_id(self, shard_id):
        try:
            return self.db_pattern % shard_id
        except TypeError:
            return self.db_pattern
