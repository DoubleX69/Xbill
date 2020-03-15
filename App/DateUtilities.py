from datetime import datetime
from dateutil.relativedelta import relativedelta
from Config.config import *


class FinancialDateTime(object):
    START_DAY = START_DAY_OF_MONTH

    @classmethod
    def current_financial_month(cls) -> datetime:
        t = datetime.now()

        if t.day < cls.START_DAY:
            t = t - relativedelta(months=1)

        return t

    @classmethod
    def financial_month_range(cls, year, month) -> (datetime, datetime):
        start_time = datetime(year, month, cls.START_DAY)
        t = start_time + relativedelta(months=1) - relativedelta(days=1)
        end_time = datetime(t.year, t.month, t.day, 23, 59, 59)
        return start_time, end_time

    @classmethod
    def year_range(cls, year) -> (datetime, datetime):
        end_time = datetime(year, 12, 31, 0, 0, 0, 0)
        start_time = datetime(year, 1, 1, 0, 0, 0, 0)
        return start_time, end_time
