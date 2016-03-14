from peewee import IntegerField


class UnsignedBigIntegerField(IntegerField):
    db_field = 'bigint unsigned'
