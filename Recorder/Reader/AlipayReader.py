from typing import Optional

from .BaseReader import BaseReader
from Models.AlipayBill import AlipayBill

from Helper.Utilities import *

import csv


class AlipayReader(BaseReader):
    titles = ['交易号', '商家订单号', '交易创建时间', '付款时间', '最近修改时间', '交易来源地', '类型', '交易对方', '商品名称', '金额（元）', '收/支', '交易状态',
              '服务费（元）', '成功退款（元）', '备注', '资金状态']

    def __init__(self, file_path):
        super(AlipayReader, self).__init__(file_path)

    def is_standard_file(self, row=None) -> bool:
        if row is None:
            row = []
        if len(row) < len(self.titles):
            return False
        else:
            for idx in range(len(self.titles)):
                if self.titles[idx] not in row[idx]:
                    return False
            return True

    def read_line(self, row=None) -> Optional[AlipayBill]:
        if row is None:
            row = []
        if len(row) < len(self.titles):
            return None
        else:
            record = AlipayBill()
            record.trans_id = row[0].strip()
            record.order_id = row[1].strip()
            record.create_time = str_to_datetime(row[2].strip())
            record.modify_time = str_to_datetime(row[4].strip())
            record.source = row[5].strip()
            record.trans_type = row[6].strip()
            record.trader_name = row[7].strip()
            record.product_name = row[8].strip()
            record.amount = float(row[9].strip())
            record.trans_status = row[10].strip()
            record.service_fee = float(row[12].strip())
            record.remarks = row[14].strip()
            record.fund_status = row[15].strip()
            return record

    def read(self):
        records = []
        is_standard = False
        with open(self.file_path, encoding='GBK') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if self.is_standard_file(row):
                    is_standard = True
                    break
            if is_standard:
                for row in reader:
                    record = self.read_line(row)
                    if record is not None:
                        records.append(record)
        records.reverse()
        return records
