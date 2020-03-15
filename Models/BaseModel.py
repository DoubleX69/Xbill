from peewee import *

database = SqliteDatabase('account.db', pragmas={'journal_mode': 'wal', 'cache_size': -1024 * 64})


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database
