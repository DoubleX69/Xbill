from peewee import *


database = SqliteDatabase('account.db', pragmas={'journal_mode': 'wal', 'cache_size': -1024 * 64})


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database


class BillModel(Model):
    class Meta:
        database = database

    def to_xbill(self) -> "XBill":
        raise NotImplementedError

    def is_exist(self) -> bool:
        raise NotImplementedError

    def save_if_no_exist(self) -> bool:
        if not self.is_exist():
            return self.save()
        else:
            return False

    @classmethod
    def create_from_row(cls, row) -> "BillModel":
        raise NotImplementedError
