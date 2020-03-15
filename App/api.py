from Models.AlipayBill import AlipayBill

from Models.XBill import *
from .DateUtilities import *
from .DataModel import *
from .Extractor import *
from .ChartModel import *
from .Statistician import Statistician
from Recorder.RecordFactory import get_recorder
from Config.config import *


def read_csv(file_path: str) -> str:
    recorder = get_recorder(file_path)
    count = 0
    if recorder is not None:
        count = recorder.save()
    s = "insert {} bills to database...".format(count)

    print(s)
    return s


def draw_balance_bar_in_month(year, month) -> Bar:
    start_time, end_time = FinancialDateTime.financial_month_range(year, month)
    query = XBill.query_with_date_range(start_time, end_time)

    balance_axis = DayExtractor.extract_balance(start_time, end_time, query)

    return draw_balance_bar(balance_axis, title='月度收支')


def draw_balance_bar_per_month(year) -> Bar:
    start_time, end_time = FinancialDateTime.year_range(year)
    query = XBill.query_with_date_range(start_time, end_time)
    balance_axis = MonthExtractor.extract_balance(start_time, end_time, query)
    return draw_balance_bar(balance_axis, title='年度收支', markline=BUDGET_OF_MONTH)


def draw_balance_bar_per_year() -> Bar:
    query = XBill.select().order_by(XBill.trans_time)
    balance_axis = YearExtractor.extract_balance(query)
    return draw_balance_bar(balance_axis, title="年度对比", markline=BUDGET_OF_MONTH * 12)


def draw_investment_bar_in_month(year, month) -> Bar:
    start_time, end_time = FinancialDateTime.financial_month_range(year, month)
    query = XBill.query_with_date_range(start_time, end_time)

    balance_axis = DayExtractor.extract_investment(start_time, end_time, query)

    return draw_balance_bar(balance_axis, title='月度理财')


def draw_surplus_line_per_year() -> Line:
    query = XBill.select().order_by(XBill.trans_time)
    axis = YearExtractor.extract_surplus(query)
    return draw_surplus_line(axis)


def draw_pie_per_month(year, month) -> Pie:
    start_time, end_time = FinancialDateTime.financial_month_range(year, month)
    query = XBill.query_with_date_range(start_time, end_time)

    pie_axis = MonthExtractor.extract_category_balance(query)

    return draw_category_pie(pie_axis)


def draw_pie_per_year(year) -> Pie:
    start_time, end_time = FinancialDateTime.year_range(year)
    query = XBill.query_with_date_range(start_time, end_time)

    pie_axis = YearExtractor.extract_category_balance(query)

    return draw_category_pie(pie_axis)


def account_status_per_month(year, month, prefix='本月') -> dict:
    start_time, end_time = FinancialDateTime.financial_month_range(year, month)
    query = XBill.query_with_date_range(start_time, end_time)
    s = Statistician(query)
    status = s.account_status(prefix)

    return status


def account_status_per_year(year, prefix='本年') -> dict:
    start_time, end_time = FinancialDateTime.year_range(year)
    query = XBill.query_with_date_range(start_time, end_time)
    s = Statistician(query, budget=BUDGET_OF_MONTH * 12)
    status = s.account_status(prefix)

    return status


def sum_of_month_payout(year, month) -> float:
    start_time, end_time = FinancialDateTime.financial_month_range(year, month)
    query = XBill.query_with_date_range(start_time, end_time)
    s = Statistician(query)

    payout = s.sum_payout()

    return float(payout)


def draw_month_usage(year, month) -> Pie:
    start_time, end_time = FinancialDateTime.financial_month_range(year, month)
    query = XBill.query_with_date_range(start_time, end_time)
    s = Statistician(query)

    payout = s.sum_payout()

    surplus = float(BUDGET_OF_MONTH - payout)
    payout = float(payout)
    if surplus < 0:
        surplus = 0

    data = [('结余', surplus), ('支出', payout)]

    return draw_usage_pie(payout=data, budget=[('预算', BUDGET_OF_MONTH)], title="本月结余")


def get_balance_details_in_month(year, month) -> (list, list):
    start_time, end_time = FinancialDateTime.financial_month_range(year, month)

    q = XBill.query_with_date_range(start_time, end_time)

    visual_xbills = []
    for xbill in q:
        d = xbill.to_dict()
        visual_xbills.append(d)

    return visual_xbills, XBill.get_columns_setting()


def account_surplus_from_start_to_now() -> float:
    query = XBill.select().order_by(XBill.trans_time)
    s = Statistician(query)
    surplus = s.sum_income() - s.sum_payout()

    return float(surplus)
