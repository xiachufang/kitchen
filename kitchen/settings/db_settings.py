step = 1
host_settings = [
    {'range': list(range(step * 0, step * 1)), 'master': 'localhost', 'slave': ''},
    {'range': list(range(step * 1, step * 2)), 'master': 'localhost', 'slave': ''},
    {'range': list(range(step * 2, step * 3)), 'master': 'localhost', 'slave': ''},
    {'range': list(range(step * 3, step * 4)), 'master': 'localhost', 'slave': ''},
    {'range': list(range(step * 4, step * 5)), 'master': 'localhost', 'slave': ''},
    {'range': list(range(step * 5, step * 6)), 'master': 'localhost', 'slave': ''},
    {'range': list(range(step * 6, step * 7)), 'master': 'localhost', 'slave': ''},
    {'range': list(range(step * 7, step * 8)), 'master': 'localhost', 'slave': ''},
]
total_shards = len(host_settings) * step

shard_settings = {
    'db_pattern': 'db%05d',
    'user': 'root',
    'password': '',
    'total_shards': total_shards,
    'hosts': host_settings,
}
