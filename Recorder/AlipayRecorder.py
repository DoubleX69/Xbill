from typing import NoReturn

from Recorder.BaseRecorder import BaseRecorder
from .Reader.AlipayReader import AlipayReader
from Config.const import BillStatus


class AlipayRecorder(BaseRecorder):

    def __init__(self, file_path):
        super(AlipayRecorder, self).__init__(file_path)

    def save(self) -> int:
        alipay_bills = AlipayReader(self.file_path).read()
        count = 0
        for bill in alipay_bills:
            if bill.save_if_no_exist():
                xbill = bill.to_xbill()
                if xbill.save():
                    self.update_same_xbill(xbill, xbill.get_same())
                    count += 1
                else:
                    raise ValueError("the xbill save failed!!", str(xbill))

        return count

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
