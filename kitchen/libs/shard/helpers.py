def make_unique_id(shard_id, type_id, local_id):
    '''64bit unique id, the first 2 bits are reserved'''
    id = (shard_id << 46) | (type_id << 36) | (local_id << 0)
    return id


def parse_unique_id(unique_id):
    shard_id = (unique_id >> 46) & 0xFFFF
    type_id = (unique_id >> 36) & 0x3FF
    local_id = (unique_id >> 0) & 0xFFFFFFFFF
    return shard_id, type_id, local_id
