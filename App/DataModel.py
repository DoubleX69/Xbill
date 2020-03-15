from typing import Sequence, Dict


class BalanceAxis(object):

    def __init__(self, x_axis: Sequence, y_axis: Dict[str, Sequence]):
        self.x_axis = x_axis
        self.y_axis = y_axis


class SurplusAxis(object):

    def __init__(self, x_date, y_surplus):
        self.x_date = x_date
        self.y_surplus = y_surplus


class PieAxis(object):

    def __init__(self, inner_data, outer_data):
        self.inner_data = inner_data
        self.outer_data = outer_data
