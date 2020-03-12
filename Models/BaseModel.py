from peewee import *

database = MySQLDatabase('accounting', **{'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '****'})


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database
