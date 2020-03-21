from .BaseModel import database
from .AlipayBill import AlipayBill
from .ICBCBill import ICBCBill
from .XBill import XBill


def create_table():
    database.create_tables([AlipayBill, ICBCBill, XBill], safe=True)
