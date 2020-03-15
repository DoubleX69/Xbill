from datetime import timedelta

from Models.XBill import *
from .DateUtilities import *
from .DataModel import *


class DayExtractor(object):

    @classmethod
    def extract_balance(cls, start_time: datetime, end_time: datetime, query: list) -> BalanceAxis:

        delta = (end_time - start_time).days + 1

        attr_date = []
        for i in range(delta):
            x = start_time + timedelta(days=i)
            x = x.strftime("%m-%d")
            attr_date.append(x)

        attr_payout = [0] * len(attr_date)
        for i in range(delta):
            x = start_time + timedelta(days=i)
            for bill in query:
                if bill.is_payout() and bill.trans_time.date() == x.date():
                    attr_payout[i] = attr_payout[i] + bill.amount

        attr_income = [0] * len(attr_date)
        for i in range(delta):
            x = start_time + timedelta(days=i)
            for bill in query:
                if bill.is_income() and bill.trans_time.date() == x.date():
                    attr_income[i] = attr_income[i] + bill.amount

        attr_payout = [float(x) for x in attr_payout]
        attr_income = [float(x) for x in attr_income]

        y_axis = {'支出': attr_payout, '收入': attr_income}

        return BalanceAxis(attr_date, y_axis)

    @classmethod
    def extract_investment(cls, start_time: datetime, end_time: datetime, query: list):
        delta = (end_time - start_time).days + 1

        attr_date = []
        for i in range(delta):
            x = start_time + timedelta(days=i)
            x = x.strftime("%m-%d")
            attr_date.append(x)

        attr_fund = [0] * len(attr_date)
        for i in range(delta):
            x = start_time + timedelta(days=i)
            bill: XBill
            for bill in query:
                if bill.is_fund() and bill.trans_time.date() == x.date():
                    attr_fund[i] = attr_fund[i] + bill.amount

        attr_ransom = [0] * len(attr_date)
        for i in range(delta):
            x = start_time + timedelta(days=i)
            for bill in query:
                if bill.is_ransom() and bill.trans_time.date() == x.date():
                    attr_ransom[i] = attr_ransom[i] + bill.amount

        attr_fund = [float(x) for x in attr_fund]
        attr_ransom = [float(x) for x in attr_ransom]

        y_axis = {'投资': attr_fund, '赎回': attr_ransom}

        return BalanceAxis(attr_date, y_axis)


class MonthExtractor(object):

    @classmethod
    def extract_balance(cls, start_time: datetime, end_time: datetime, query: list) -> BalanceAxis:

        delta = end_time.month - start_time.month + 1

        attr_date = []
        for i in range(delta):
            attr_date.append('{}月'.format(i + 1))

        attr_payout = [0] * len(attr_date)
        for i in range(delta):
            x = i + 1
            for bill in query:
                if bill.is_payout() and bill.trans_time.date().month == x:
                    attr_payout[i] = attr_payout[i] + bill.amount

        attr_income = [0] * len(attr_date)

        for i in range(delta):
            x = i + 1
            for bill in query:
                if bill.is_income() and bill.trans_time.date().month == x:
                    attr_income[i] = attr_income[i] + bill.amount

        attr_payout = [float(x) for x in attr_payout]
        attr_income = [float(x) for x in attr_income]

        y_axis = {'支出': attr_payout, '收入': attr_income}

        return BalanceAxis(attr_date, y_axis)

    @classmethod
    def extract_category_balance(cls, query: list) -> PieAxis:

        sum_with_category = dict()

        xbill: XBill
        for xbill in query:
            if xbill.is_payout():
                category = xbill.category
                if category in sum_with_category:
                    sum_with_category[category] += xbill.amount
                else:
                    sum_with_category[category] = xbill.amount

        data = []
        for k, v in sum_with_category.items():
            data.append((k, float(v)))

        sum_with_subcategory = dict()

        for category in sum_with_category.keys():
            for xbill in query:
                if category == xbill.category and xbill.is_payout():
                    all_category = "{}-{}".format(xbill.category, xbill.subcategory)
                    if all_category in sum_with_subcategory:
                        sum_with_subcategory[all_category] += xbill.amount
                    else:
                        sum_with_subcategory[all_category] = xbill.amount

        out_data = []
        for k, v in sum_with_subcategory.items():
            out_data.append((k, float(v)))

        return PieAxis(inner_data=data, outer_data=out_data)


class YearExtractor(object):
    @classmethod
    def extract_balance(cls, query: list) -> BalanceAxis:
        payout_per_year = {}
        income_per_year = {}

        for xbill in query:
            year = xbill.trans_time.year
            if xbill.is_payout():
                if year in payout_per_year.keys():
                    payout_per_year[year] = payout_per_year[year] + xbill.amount
                else:
                    payout_per_year[year] = xbill.amount
            elif xbill.is_income():
                if year in income_per_year.keys():
                    income_per_year[year] = income_per_year[year] + xbill.amount
                else:
                    income_per_year[year] = xbill.amount

            else:
                pass

        payout_years = [x for x in payout_per_year.keys()]
        payout_sum = [float(x) for x in payout_per_year.values()]

        income_years = [x for x in income_per_year.keys()]
        income_sum = [float(x) for x in income_per_year.values()]

        y_axis = {'支出': payout_sum, '收入': income_sum}

        return BalanceAxis(payout_years, y_axis)

    @classmethod
    def extract_surplus(cls, query: list) -> SurplusAxis:
        payout_per_year = {}
        income_per_year = {}

        for xbill in query:
            year = xbill.trans_time.year
            if xbill.is_payout():
                if year in payout_per_year.keys():
                    payout_per_year[year] = payout_per_year[year] + xbill.amount
                else:
                    payout_per_year[year] = xbill.amount
            elif xbill.is_income():
                if year in income_per_year.keys():
                    income_per_year[year] = income_per_year[year] + xbill.amount
                else:
                    income_per_year[year] = xbill.amount

            else:
                pass

        payout_years = [x for x in payout_per_year.keys()]
        payout_sum = [x for x in payout_per_year.values()]

        income_years = [x for x in income_per_year.keys()]
        income_sum = [x for x in income_per_year.values()]

        balance_sum = []
        for i in range(len(payout_sum)):
            balance_sum.append(income_sum[i] - payout_sum[i])

        income_years = [str(x) for x in income_years]
        balance_sum = [float(x) for x in balance_sum]

        return SurplusAxis(income_years, balance_sum)

    @classmethod
    def extract_category_balance(cls, query: list) -> PieAxis:

        sum_with_category = dict()

        xbill: XBill
        for xbill in query:
            if xbill.is_payout():
                category = xbill.category
                if category in sum_with_category:
                    sum_with_category[category] += xbill.amount
                else:
                    sum_with_category[category] = xbill.amount

        data = []
        for k, v in sum_with_category.items():
            data.append((k, float(v)))

        sum_with_subcategory = dict()

        for category in sum_with_category.keys():
            for xbill in query:
                if category == xbill.category and xbill.is_payout():
                    all_category = "{}-{}".format(xbill.category, xbill.subcategory)
                    if all_category in sum_with_subcategory:
                        sum_with_subcategory[all_category] += xbill.amount
                    else:
                        sum_with_subcategory[all_category] = xbill.amount

        out_data = []
        for k, v in sum_with_subcategory.items():
            out_data.append((k, float(v)))

        return PieAxis(inner_data=data, outer_data=out_data)
