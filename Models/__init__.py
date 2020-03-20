from .BaseModel import database
from .AlipayBill import AlipayBill
from .XBill import XBill


def create_table():
    database.create_tables([AlipayBill, XBill], safe=True)
