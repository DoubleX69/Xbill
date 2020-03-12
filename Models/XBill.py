from .BaseModel import *

from datetime import datetime

from Helper import Utilities


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

    def set_record(self, **kwargs):
        self.id = kwargs['id']
        self.account = kwargs['account']
        self.amount = kwargs['amount']
        self.trans_time = kwargs['trans_time']
        self.status = kwargs['status']
        self.category = kwargs['category']
        self.subcategory = kwargs['subcategory']
        self.trader_name = kwargs['trader_name']
        self.product_name = kwargs['product_name']
        self.remarks = kwargs['remarks']
        self.associate_id = kwargs['associate_id']

    def same_of(self, other, account):
        self.account = account
        self.trans_time = other.trans_time
        self.status = '内部转账'
        self.category = '转移'
        self.subcategory = ''
        self.associate_id = other.id

    def to_visual_list(self):
        return [self.account, self.status, self.amount, self.category, self.product_name]

    def insert_record(self):
        return self.save()

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
        if self.status == "支出":
            if self.category == '投资':
                return False
            else:
                return True
        else:
            return False

    def is_income(self):

        if self.valid and self.status == "收入":
            if self.category == '赎回':
                return False
            else:
                return True
        else:
            return False

    def is_fund(self):
        if self.valid and self.status == "支出":
            if self.category == '投资':
                return True
            else:
                return False
        else:
            return False

    def is_ransom(self):
        if self.valid and self.status == "收入":
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

# class XBillTableWrapper(object):
#
#     def __init__(self, database):
#         self.database = DataBaseWrapper(database)
#
#     @classmethod
#     def insert_record(cls, record):
#         try:
#             ret = XBill.create(
#                 account=record.account,
#                 amount=record.amount,
#                 trans_time=record.trans_time,
#                 status=record.status,
#                 category=record.category,
#                 subcategory=record.subcategory,
#                 trader_name=record.trader_name,
#                 product_name=record.product_name,
#                 remarks=record.remarks,
#                 associate_id=record.associate_id)
#         except IntegrityError:
#             print("insert record to mybill table Error")
#             ret = None
#     #     return ret
#     #
#     # @classmethod
#     # def is_record_exist(cls, ):
#     #     l = []
#     #     query = XBill.select().where(
#     #         (XBill.account == record.account) &
#     #         (XBill.amount == record.amount) &
#     #         (XBill.status == record.status) &
#     #         (XBill.trans_time == record.trans_time)
#     #     ).dicts()
#     #     for item in query:
#     #         l.append(item)
#     #     if l:
#     #         return True
#     #     else:
#     #         return False
#     #
#     # @classmethod
#     # def get_max_id(cls):
#     #     query = XBill.select(fn.MAX(XBill.id))
#     #     max_id = query.scalar()
#     #     return max_id
#     #
#     # @classmethod
#     # def query_great_id(cls, id):
#     #     query = XBill.select().where(XBill.id > id).order_by(XBill.id).dicts()
#     #
#     #     l = []
#     #     for item in query:
#     #         xbill = XBillRecord()
#     #         xbill.set_record(**item)
#     #         l.append(xbill)
#     #     return l
#
#     @classmethod
#     def query_after_day(cls, day):
#         query = XBill.select().where(XBill.trans_time >= day).order_by(XBill.trans_time)
#         query = query.dicts()
#
#         l = []
#         for item in query:
#             xbill = XBillRecord()
#             xbill.set_record(**item)
#             l.append(xbill)
#         return l
#
#     @classmethod
#     def query_with_date_range(cls, start_time, end_time):
#         start_time = datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0, 0)
#         end_time = datetime(end_time.year, end_time.month, end_time.day, 0, 0, 0, 0)
#
#         query = XBill.select().where(
#             (XBill.trans_time >= start_time) &
#             (XBill.trans_time < end_time)).order_by(XBill.trans_time.desc())
#         query = query.dicts()
#
#         ret = []
#         for item in query:
#             xbill = XBillRecord()
#             xbill.set_record(**item)
#             ret.append(xbill)
#         return ret
#
#     @classmethod
#     def query_same_xbills(cls, account, record):
#         start_day = record.trans_time.date()
#         start_time = datetime(start_day.year, start_day.month, start_day.day, 0, 0, 0, 0)
#         end_time = datetime(start_day.year, start_day.month, start_day.day, 23, 59, 59, 0)
#         query = XBill.select().where(
#             (XBill.trans_time.between(start_time, end_time)) &
#             (XBill.amount == record.amount) &
#             (~(XBill.account == account))
#         ).order_by(XBill.trans_time)
#         query = query.dicts()
#
#         ret = []
#         for item in query:
#             xbill = XBillRecord()
#             xbill.set_record(**item)
#             ret.append(xbill)
#         return ret
#
#     @classmethod
#     def update_by_id(self, record):
#         update = XBill.update(account=record.account,
#                               amount=record.amount,
#                               trans_time=record.trans_time,
#                               status=record.status,
#                               category=record.category,
#                               subcategory=record.subcategory,
#                               trader_name=record.trader_name,
#                               product_name=record.product_name,
#                               remarks=record.remarks,
#                               associate_id=record.associate_id).where(XBill.id == record.id).execute()
#
#         return update
