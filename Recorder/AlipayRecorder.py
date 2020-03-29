from typing import NoReturn

from Recorder.BaseRecorder import BaseRecorder
from Config.const import BillStatus
from Models.AlipayBill import AlipayBill


class AlipayRecorder(BaseRecorder):

    def __init__(self, rows):
        super(AlipayRecorder, self).__init__(rows, AlipayBill)

    @classmethod
    def update_same_xbill(cls, xbill, same_xbills) -> NoReturn:
        for same in same_xbills:
            if '->' not in same.account and same.account != xbill.account:
                if same.status == BillStatus.PAYOUT:
                    same.same_of(xbill, same.account + '->' + xbill.account)
                elif same.status == BillStatus.INCOME and xbill.status == BillStatus.INTERNAL_TRANS:
                    account = xbill.account + "->" + same.account
                    same.same_of(xbill, account)
                    xbill.account = account
                    xbill.save()
                elif same.status == BillStatus.INCOME and xbill.status == BillStatus.INCOME:
                    account = xbill.account + "->" + same.account
                    same.same_of(xbill, account)
                    same.status = '退款'
                    xbill.account = account
                    xbill.status = BillStatus.INTERNAL_TRANS
                    xbill.save()
                else:
                    print(xbill, same)
                    raise NotImplementedError("this condition is not implemented")
                same.save()
                break
