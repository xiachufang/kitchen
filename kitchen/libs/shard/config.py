import operator
from functools import reduce


class ShardConfig:
    def __init__(self, hosts, **db_config):
        '''
        settings:
            [
                {'range': range(0, 511), 'master': 'MySQL001A', 'slave': 'MySQL001B'},
                {'range': range(512, 1023), 'master': 'MySQL002A', 'slave': 'MySQL002B'},
                {'range': range(3584, 4095), 'master': 'MySQL008A', 'slave': 'MySQL008B'}
            ]
        '''
        self.hosts = hosts
        self.db_config = db_config
        self.shard_ids = reduce(operator.concat, map(operator.itemgetter('range'), hosts))

    def get_host_by_shard_id(self, shard_id):
        for s in self.hosts:
            if shard_id in s['range']:
                return s
        raise ValueError('no shard_id %s' % shard_id)

    def get_db_name_by_shard_id(self, shard_id):
        return 'db%05d' % shard_id
