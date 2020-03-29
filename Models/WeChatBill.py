from Helper.Utilities import *
from .BaseModel import *
from .XBill import XBill
from Classifier.Classifier import Classifier
from Config.const import BillStatus


class WeChatBill(BillModel):
    id = AutoField(primary_key=True, column_name='id')

    trans_time = DateTimeField(column_name='trans_time')
    trans_type = CharField(30, column_name='trans_type')
    trader_name = CharField(60, column_name='trader_name')
    product_name = CharField(150, column_name='product_name')
    fund_status = FixedCharField(15, column_name='fund_status')
    amount = DecimalField(max_digits=10, decimal_places=2, column_name='amount')
    pay_type = CharField(60, column_name='pay_type')
    trans_status = FixedCharField(30, column_name='trans_status')

    trans_id = CharField(50, column_name='trans_id', unique=True)
    trader_id = CharField(50, column_name='trader_id')

    remarks = TextField(column_name='remarks', null=True)

    account = '微信'
    titles = ['交易时间', '交易类型', '交易对方', '商品', '收/支', '金额(元)', '支付方式', '当前状态', '交易单号', '商户单号', '备注']

    class Meta:
        db_table = 'wechat'

    def __str__(self):
        return str(self.__data__)

    def to_xbill(self) -> XBill:

        def unify_status(fund_status):
            if '支出' in fund_status:
                status = BillStatus.PAYOUT
            elif '收入' in fund_status:
                status = BillStatus.INCOME
            else:
                status = BillStatus.INTERNAL_TRANS
            return status

        def format_remarks(*args) -> str:
            s = [v for v in args if v != '/']
            return ';'.join(s)

        xbill = XBill()
        xbill.account = self.account
        xbill.amount = self.amount
        xbill.currency = '人民币'
        xbill.trans_time = self.trans_time
        xbill.status = unify_status(self.fund_status)
        xbill.trader_name = self.trader_name
        xbill.product_name = self.product_name
        xbill.remarks = format_remarks(self.pay_type, self.trans_type, self.trans_status, self.remarks)
        xbill.associate_id = -1

        xbill.status, xbill.category, xbill.subcategory = Classifier().classify(xbill)
        return xbill

    def is_exist(self) -> bool:
        query = self.__class__.get_or_none(trans_id=self.trans_id)
        ret = True if query else False
        return ret

    @classmethod
    def create_from_row(cls, row) -> "WeChatBill":
        def to_float(s: str) -> float:
            s = remove_comma(s)
            s = s.replace('¥', '')
            return float(s)

        bill = WeChatBill()
        bill.trans_time = str_to_datetime(row[0].strip())
        bill.trans_type = row[1].strip()
        bill.trader_name = row[2].strip()
        bill.product_name = row[3].strip()
        bill.fund_status = row[4].strip()
        bill.amount = to_float(row[5].strip())
        bill.pay_type = row[6].strip()
        bill.trans_status = row[7].strip()

        bill.trans_id = row[8].strip()
        bill.trader_id = row[9].strip()
        bill.remarks = row[10].strip()
        return bill
