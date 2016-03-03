step = 1
shard_settings = [
    {'range': list(range(step * 0, step * 1)), 'master': 'mysql+pymysql://root:@localhost', 'slave': ''},
    {'range': list(range(step * 1, step * 2)), 'master': 'mysql+pymysql://root:@localhost', 'slave': ''},
    {'range': list(range(step * 2, step * 3)), 'master': 'mysql+pymysql://root:@localhost', 'slave': ''},
    {'range': list(range(step * 3, step * 4)), 'master': 'mysql+pymysql://root:@localhost', 'slave': ''},
    {'range': list(range(step * 4, step * 5)), 'master': 'mysql+pymysql://root:@localhost', 'slave': ''},
    {'range': list(range(step * 5, step * 6)), 'master': 'mysql+pymysql://root:@localhost', 'slave': ''},
    {'range': list(range(step * 6, step * 7)), 'master': 'mysql+pymysql://root:@localhost', 'slave': ''},
    {'range': list(range(step * 7, step * 8)), 'master': 'mysql+pymysql://root:@localhost', 'slave': ''},
]
