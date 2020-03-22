from typing import Optional

from .BaseReader import BaseReader
from Models.AlipayBill import AlipayBill

from Helper.Utilities import *


class AlipayReader(BaseReader):

    titles = ['交易号', '商家订单号', '交易创建时间', '付款时间', '最近修改时间', '交易来源地', '类型', '交易对方', '商品名称', '金额（元）', '收/支', '交易状态',
              '服务费（元）', '成功退款（元）', '备注', '资金状态']

    def __init__(self, rows):
        super(AlipayReader, self).__init__(rows)

    def to_model(self, row):
        bill = AlipayBill()
        bill.trans_id = row[0].strip()
        bill.order_id = row[1].strip()
        bill.create_time = str_to_datetime(row[2].strip())
        bill.modify_time = str_to_datetime(row[4].strip())
        bill.source = row[5].strip()
        bill.trans_type = row[6].strip()
        bill.trader_name = row[7].strip()
        bill.product_name = row[8].strip()
        bill.amount = float(row[9].strip())
        bill.trans_status = row[10].strip()
        bill.service_fee = float(row[12].strip())
        bill.remarks = row[14].strip()
        bill.fund_status = row[15].strip()
        return bill
