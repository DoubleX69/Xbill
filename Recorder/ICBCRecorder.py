from peewee import PeeweeException

from Recorder.BaseRecorder import BaseRecorder
from Recorder.Reader.ICBCReader import ICBCReader

from typing import NoReturn
from Models import database


class ICBCRecorder(BaseRecorder):

    def __init__(self, data):
        super(ICBCRecorder, self).__init__(data)

    def save(self) -> int:
        count = 0
        icbc_bills = ICBCReader(self.rows).read()
        with database.transaction() as tr:
            try:
                for bill in icbc_bills:
                    if bill.save_if_no_exist():
                        xbill = bill.to_xbill()
                        if xbill.save():
                            self.update_same_xbill(xbill, xbill.get_same())
                            count += 1
                        else:
                            print("the xbill save failed!!", str(xbill))
                    else:
                        print("{} is exist".format(str(bill)))
            except PeeweeException:
                tr.rollback()
                print("load csv file Error! Not insert into database!!")
                count = 0

        return count

    @classmethod
    def update_same_xbill(cls, xbill, same_xbills) -> NoReturn:
        for same in same_xbills:
            if '->' not in same.account and same.account != xbill.account:
                if xbill.status == "支出":
                    xbill.same_of(same, xbill.account + '->' + same.account)
                elif same.status == "内部转账" and xbill.status == "收入":
                    account = same.account + "->" + xbill.account
                    xbill.same_of(xbill, account)
                    same.account = account
                    same.save()
                elif same.status == "收入" and xbill.status == "收入":
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
