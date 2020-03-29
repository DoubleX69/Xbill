from .Reader.BaseReader import BaseReader
from Models import BillModel, database

from peewee import PeeweeException


class BaseRecorder(object):

    def __init__(self, rows, model):
        self.rows = rows
        self.model = model

        if not issubclass(self.model, BillModel):
            raise ValueError("model must be extend from BillModel!")

        if not hasattr(self.model, "titles"):
            raise ValueError("model must has 'titles' attr!")

    def save(self) -> int:
        bills = BaseReader(self.rows, self.model).read()

        if not bills:
            return 0

        count = 0
        with database.transaction() as tr:
            try:
                for bill in bills:
                    if bill.save_if_no_exist():
                        xbill = bill.to_xbill()
                        if xbill.save():
                            self.update_same_xbill(xbill, xbill.get_same())
                            count += 1
                        else:
                            print(ValueError("the xbill save failed!!", str(xbill)))
            except PeeweeException:
                tr.rollback()
                count = 0
        return count

    def get_model_name(self) -> str:
        return self.model.account

    def update_same_xbill(self, xbill, same_xbills):
        raise NotImplementedError
