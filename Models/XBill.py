from .BaseModel import *

from datetime import datetime

from Helper import Utilities
from Config.const import BillStatus


class XBill(BaseModel):
    id = AutoField(primary_key=True, column_name='id')
    account = CharField(10, column_name='account')
    amount = DecimalField(max_digits=10, decimal_places=2, column_name='amount')
    currency = CharField(5, default='人民币', column_name='currency')
    trans_time = DateTimeField(column_name='trans_time')
    status = FixedCharField(15, column_name='status')
    category = FixedCharField(12, column_name='category')
    subcategory = FixedCharField(12, column_name='subcategory', default='')
    trader_name = CharField(90, column_name='trader_name')
    product_name = CharField(150, column_name='product_name')
    remarks = TextField(column_name='remarks', null=True)
    associate_id = IntegerField(column_name='associate_id', default=-1)
    valid = BooleanField(column_name='valid', default=True)

    class Meta:
        db_table = 'xbill'

    def __str__(self):
        return str(self.__data__)

    def __eq__(self, other):
        if self.amount == other.amount and self.trans_time.date() == other.trans_time.date():
            return True
        else:
            return False

    def same_of(self, other, account):
        self.account = account
        self.trans_time = other.trans_time
        self.status = BillStatus.INTERNAL_TRANS
        self.category = '转移'
        self.subcategory = ''
        self.associate_id = other.id


    def get_same(self):
        start_day = self.trans_time.date()
        start_time = datetime(start_day.year, start_day.month, start_day.day, 0, 0, 0, 0)
        end_time = datetime(start_day.year, start_day.month, start_day.day, 23, 59, 59, 0)

        query = XBill.select().where((XBill.trans_time.between(start_time, end_time)) &
                                     (XBill.amount == self.amount) &
                                     (XBill.currency == self.currency) &
                                     (~(XBill.account == self.account))).order_by(XBill.trans_time)

        ret = [x for x in query]
        return ret

    @classmethod
    def query_all(cls):
        query = XBill.select().order_by(XBill.trans_time)
        query = [x for x in query]

        return query

    @classmethod
    def query_after_day(cls, day):
        query = XBill.select().where(XBill.trans_time >= day).order_by(XBill.trans_time)
        query = [x for x in query]
        return query

    @classmethod
    def query_with_date_range(cls, start_time: datetime, end_time: datetime):
        start_time = datetime(start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute,
                              start_time.second)
        end_time = datetime(end_time.year, end_time.month, end_time.day, end_time.hour, end_time.minute,
                            end_time.second)

        query = XBill.select().where(
            (XBill.trans_time >= start_time) &
            (XBill.trans_time < end_time)).order_by(XBill.trans_time.desc())
        query = [x for x in query]

        return query

    @classmethod
    def query_all_fund(cls) -> list:

        query = XBill.select().where((XBill.category == '投资') & (XBill.status == '支出')).order_by(
            XBill.trans_time.desc())
        query = [x for x in query]

        return query

    @classmethod
    def query_all_ransom(cls) -> list:
        query = XBill.select().where((XBill.category == '赎回')).order_by(
            XBill.trans_time.desc())
        query = [x for x in query]

        return query

    def is_payout(self):
        if self.status == BillStatus.PAYOUT:
            if self.category == '投资':
                return False
            else:
                return True
        else:
            return False

    def is_income(self):

        if self.valid and self.status == BillStatus.INCOME:
            if self.category == '赎回':
                return False
            else:
                return True
        else:
            return False

    def is_fund(self):
        if self.valid and self.status == BillStatus.PAYOUT:
            if self.category == '投资':
                return True
            else:
                return False
        else:
            return False

    def is_ransom(self):
        if self.valid and self.status == BillStatus.INCOME:
            if self.category == '赎回':
                return True
            else:
                return False
        else:
            return False

    def is_wish(self):
        if self.valid and self.category.lower() == 'wish':
            return True
        else:
            return False

    def to_dict(self):
        d = dict()
        d[self.__class__.id.column_name] = self.id
        d[self.__class__.account.column_name] = self.account
        d[self.__class__.status.column_name] = self.status
        d[self.__class__.amount.column_name] = str(self.amount)
        d[self.__class__.category.column_name] = self.category
        d[self.__class__.subcategory.column_name] = self.subcategory

        d[self.__class__.trader_name.column_name] = self.trader_name
        d[self.__class__.product_name.column_name] = self.product_name

        d[self.__class__.remarks.column_name] = self.remarks

        d[self.__class__.trans_time.column_name] = Utilities.date_to_str(self.trans_time)
        return d

    @classmethod
    def get_columns_setting(cls):

        columns_setting = [
            {
                "field": cls.trans_time.column_name,  # which is the field's name of data key
                "title": "日期",  # display as the table header's name
                "sortable": True,
            },
            {
                "field": cls.id.column_name,  # which is the field's name of data key
                "title": cls.id.column_name,  # display as the table header's name
                "sortable": True,
            },
            {
                "field": cls.account.column_name,  # which is the field's name of data key
                "title": "账户",  # display as the table header's name
                "sortable": True,
            },
            {
                "field": cls.status.column_name,  # which is the field's name of data key
                "title": "状态",  # display as the table header's name
                "sortable": True,
            },
            {
                "field": cls.amount.column_name,  # which is the field's name of data key
                "title": "金额",  # display as the table header's name
                "sortable": True,
            },
            {
                "field": cls.category.column_name,  # which is the field's name of data key
                "title": "类别",  # display as the table header's name
                "sortable": True,
            },
            {
                "field": cls.subcategory.column_name,  # which is the field's name of data key
                "title": "子类",  # display as the table header's name
                "sortable": True,
            },
            {
                "field": cls.trader_name.column_name,  # which is the field's name of data key
                "title": "交易方",  # display as the table header's name
                "sortable": True,
            },
            {
                "field": cls.product_name.column_name,  # which is the field's name of data key
                "title": "商品",  # display as the table header's name
                "sortable": True,
            },
            {
                "field": cls.remarks.column_name,  # which is the field's name of data key
                "title": "备注",  # display as the table header's name
                "sortable": False,
                # "formatter":"function(value,row,index) { return '<span style="color:#fa9f00">'+value+'</span>'}",
                "editable": {"type": "text", "title": "备注"}
            },

        ]
        return columns_setting
