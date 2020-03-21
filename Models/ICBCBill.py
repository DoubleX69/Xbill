from .BaseModel import *
from .XBill import XBill
from Classifier.Classifier import Classifier
from Helper.Utilities import *
from Config.const import BillStatus


class ICBCBill(BaseModel):
    id = AutoField(primary_key=True, column_name='id')
    trans_time = DateField(column_name='trans_time')
    summary = CharField(30, column_name='summary')
    product_name = CharField(90, column_name='product_name')
    amount = DecimalField(max_digits=10, decimal_places=2, column_name='amount')
    currency = CharField(5, default='人民币', column_name='currency')
    status = FixedCharField(15, column_name='status')
    balance = DecimalField(max_digits=10, decimal_places=2, column_name='balance')
    trader_name = CharField(90, column_name='trader_name')

    account = "工商银行"

    class Meta:
        db_table = 'icbc'

    def __str__(self):
        return str(self.__data__)

    def set_amount_with_status(self, income, payout):
        if income:
            self.amount = float(remove_comma(income))
            self.status = BillStatus.INCOME
        elif payout:
            self.amount = float(remove_comma(payout))
            self.status = BillStatus.PAYOUT
        else:
            self.amount = 0.0
            self.status = BillStatus.INTERNAL_TRANS
            print(income, payout)
            raise NotImplementedError("ICBC Unknown Status")

    def to_xbill(self):
        xbill_record = XBill()
        xbill_record.account = self.account
        xbill_record.amount = self.amount
        xbill_record.currency = self.currency
        xbill_record.trans_time = self.trans_time
        xbill_record.status = self.status
        xbill_record.trader_name = self.trader_name
        xbill_record.product_name = self.summary
        xbill_record.remarks = self.product_name
        xbill_record.associate_id = -1
        xbill_record.status, xbill_record.category, xbill_record.subcategory = Classifier().classify(xbill_record)
        return xbill_record

    def is_exist(self):
        query = self.__class__.get_or_none(product_name=self.product_name, amount=self.amount, status=self.status,
                                           balance=self.balance, trader_name=self.trader_name,
                                           trans_time=self.trans_time)
        ret = True if query else False
        return ret

    def save_if_no_exist(self):
        if not self.is_exist():
            return self.save()
        else:
            return False
