from Models.ICBCBill import ICBCBill
from .BaseReader import BaseReader
from Helper.Utilities import *

import csv


class ICBCReader(BaseReader):
    titles = ['交易日期', '摘要', '交易场所', '交易国家或地区简称', '钞/汇', '交易金额(收入)', '交易金额(支出)', '交易币种', '记账金额(收入)',
              '记账金额(支出)', '记账币种', '余额', '对方户名']

    def __init__(self, file_path):
        super(ICBCReader, self).__init__(file_path)

    def is_standard_file(self, row=None):
        if row is None:
            row = []
        if len(row) < len(self.titles):
            return False
        else:
            for i in range(len(self.titles)):
                if self.titles[i] not in row[i]:
                    return False
            return True

    def read_line(self, row=None):
        if row is None:
            row = []

        if row[0].strip() and len(row) >= len(self.titles):
            record = ICBCBill()
            record.trans_time = str_to_date(row[0].strip())
            record.summary = row[1].strip()
            record.product_name = row[2].strip()
            record.set_amount_with_status(row[8].strip(), row[9].strip())
            record.currency = row[10].strip()
            record.balance = float(remove_comma(row[11].strip()))
            record.trader_name = row[12].strip()
            record.remarks = row[1].strip()
            return record
        else:
            return None

    def read(self):
        is_standard = False
        records = []
        with open(self.file_path, encoding='UTF-8') as csv_file:
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
