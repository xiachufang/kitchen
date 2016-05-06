step = 128
host_settings = [
    {'range': list(range(step * 0, step * 1)), 'master': '172.31.1.229', 'slave': ''},
    {'range': list(range(step * 1, step * 2)), 'master': '172.31.1.229', 'slave': ''},
    {'range': list(range(step * 2, step * 3)), 'master': '172.31.1.229', 'slave': ''},
    {'range': list(range(step * 3, step * 4)), 'master': '172.31.1.229', 'slave': ''},
    {'range': list(range(step * 4, step * 5)), 'master': '172.31.1.229', 'slave': ''},
    {'range': list(range(step * 5, step * 6)), 'master': '172.31.1.229', 'slave': ''},
    {'range': list(range(step * 6, step * 7)), 'master': '172.31.1.229', 'slave': ''},
    {'range': list(range(step * 7, step * 8)), 'master': '172.31.1.229', 'slave': ''},
]
total_shards = len(host_settings) * step

shard_settings = {
    'db_pattern': 'db%05d',
    'user': 'kitchen',
    'password': '',
    'total_shards': total_shards,
    'hosts': host_settings,
}
