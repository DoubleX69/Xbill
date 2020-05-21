from Helper.Utilities import str_to_datetime
from .BaseModel import *
from .XBill import XBill
from Classifier.Classifier import Classifier
from Config.const import BillStatus


class AlipayBill(BillModel):
    id = AutoField(primary_key=True, column_name='id')
    trans_id = CharField(70, column_name='trans_id', unique=True)
    order_id = CharField(50, column_name='order_id')
    create_time = DateTimeField(column_name='create_time')
    modify_time = DateTimeField(column_name='modify_time')
    source = CharField(150, column_name='source')
    trans_type = CharField(30, column_name='trans_type')
    trader_name = CharField(60, column_name='trader_name')
    product_name = CharField(150, column_name='product_name')
    amount = DecimalField(max_digits=10, decimal_places=2, column_name='amount')
    trans_status = FixedCharField(15, column_name='trans_status')
    service_fee = DecimalField(max_digits=10, decimal_places=2, column_name='service_fee')
    fund_status = FixedCharField(15, column_name='fund_status')
    remarks = TextField(column_name='remarks', null=True)

    account = '支付宝'
    titles = ['交易号', '商家订单号', '交易创建时间', '付款时间', '最近修改时间', '交易来源地', '类型', '交易对方', '商品名称',
              '金额（元）', '收/支', '交易状态', '服务费（元）', '成功退款（元）', '备注', '资金状态']

    class Meta:
        db_table = 'alipay'

    def __str__(self):
        return str(self.__data__)

    def to_xbill(self) -> XBill:

        def unify_status(fund_status):
            if '支出' in fund_status:
                status = BillStatus.PAYOUT
            elif '收入' in fund_status:
                status = BillStatus.INCOME
            elif '资金转移' in fund_status:
                status = BillStatus.INTERNAL_TRANS
            else:
                status = fund_status
            return status

        xbill_record = XBill()
        xbill_record.account = self.account
        xbill_record.amount = self.amount + self.service_fee
        xbill_record.currency = '人民币'
        xbill_record.trans_time = self.create_time
        xbill_record.status = unify_status(self.fund_status)
        xbill_record.trader_name = self.trader_name
        xbill_record.product_name = self.product_name
        xbill_record.remarks = self.source + ';' + self.remarks
        xbill_record.associate_id = -1

        xbill_record.status, xbill_record.category, xbill_record.subcategory = Classifier().classify(xbill_record)
        return xbill_record

    def is_exist(self) -> bool:
        query = self.__class__.get_or_none(trans_id=self.trans_id)
        ret = True if query else False
        return ret

    @classmethod
    def create_from_row(cls, row) -> "AlipayBill":
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
