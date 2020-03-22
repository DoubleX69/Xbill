from Models.ICBCBill import ICBCBill
from .BaseReader import BaseReader
from Helper.Utilities import *


class ICBCReader(BaseReader):
    titles = ['交易日期', '摘要', '交易场所', '交易国家或地区简称', '钞/汇', '交易金额(收入)', '交易金额(支出)', '交易币种', '记账金额(收入)',
              '记账金额(支出)', '记账币种', '余额', '对方户名']

    def __init__(self, rows):
        super(ICBCReader, self).__init__(rows)

    def to_model(self, row):
        bill = ICBCBill()
        bill.trans_time = str_to_date(row[0].strip())
        bill.summary = row[1].strip()
        bill.product_name = row[2].strip()
        bill.set_amount_with_status(row[8].strip(), row[9].strip())
        bill.currency = row[10].strip()
        bill.balance = float(remove_comma(row[11].strip()))
        bill.trader_name = row[12].strip()
        bill.remarks = row[1].strip()
        return bill
