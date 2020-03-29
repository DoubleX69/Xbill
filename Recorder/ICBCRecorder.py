from peewee import PeeweeException

from Recorder.BaseRecorder import BaseRecorder
from Config.const import BillStatus
from typing import NoReturn
from Models.ICBCBill import ICBCBill


class ICBCRecorder(BaseRecorder):

    def __init__(self, rows):
        super(ICBCRecorder, self).__init__(rows, ICBCBill)

    @classmethod
    def update_same_xbill(cls, xbill, same_xbills) -> NoReturn:
        for same in same_xbills:
            if '->' not in same.account and same.account != xbill.account:
                if xbill.status == BillStatus.PAYOUT:
                    xbill.same_of(same, xbill.account + '->' + same.account)
                elif same.status == BillStatus.INTERNAL_TRANS and xbill.status == BillStatus.INCOME:
                    account = same.account + "->" + xbill.account
                    xbill.same_of(xbill, account)
                    same.account = account
                    same.save()
                elif same.status == BillStatus.INCOME and xbill.status == BillStatus.INCOME:
                    account = same.account + "->" + xbill.account
                    xbill.same_of(same, account)
                    same.account = account
                    same.status = '退款'
                    same.save()
                else:
                    print(xbill.product_name, xbill.amount)
                    # raise NotImplementedError("this condition is not implemented")
                xbill.save()
                break
