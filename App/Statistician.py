from typing import List

from Models.XBill import *


class Statistician(object):

    def __init__(self, query: List[XBill], budget=7000):
        self.query = query
        self.budget = budget

    def sum_wish(self) -> float:
        sum_val = 0
        for xbill in self.query:
            if xbill.is_wish():
                sum_val += xbill.amount
        return sum_val

    def sum_income(self) -> float:
        sum_val = 0
        for xbill in self.query:
            if xbill.is_income():
                sum_val += xbill.amount
        return sum_val

    def sum_payout(self):
        sum_val = 0
        for xbill in self.query:
            if xbill.is_payout():
                sum_val += xbill.amount
        return sum_val

    def sum_fund(self) -> float:
        sum_val = 0
        for xbill in self.query:
            if xbill.is_fund():
                sum_val += xbill.amount
        return sum_val

    def sum_ransom(self) -> float:
        sum_val = 0
        for xbill in self.query:
            if xbill.is_ransom():
                sum_val += xbill.amount
        return sum_val

    def account_status(self, prefix) -> dict:

        income = self.sum_income()
        payout = self.sum_payout()
        fund = self.sum_fund()
        ransom = self.sum_ransom()
        wish = self.sum_wish()

        status = dict()
        status[prefix + "收入"] = float(income)
        status[prefix + "支出"] = float(payout)
        status[prefix + "预算"] = float(self.budget - payout)
        status[prefix + "结余"] = float(income - payout)
        status[prefix + "投资"] = float(fund)
        status[prefix + "赎回"] = float(ransom)
        status[prefix + "心愿支出"] = float(wish)

        return status
