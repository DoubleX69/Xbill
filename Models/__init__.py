from .BaseModel import database, BillModel
from .AlipayBill import AlipayBill
from .WeChatBill import WeChatBill
from .ICBCBill import ICBCBill
from .XBill import XBill


def create_table():
    database.create_tables([AlipayBill, WeChatBill, ICBCBill, XBill], safe=True)
