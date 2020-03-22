class BaseReader(object):
    titles = ['Base']

    def __init__(self, rows):
        self.rows = rows
        self.start = -1
        self.end = -1

    def is_title_row(self, row=None) -> bool:
        if row is None:
            return False

        if len(row) < len(self.titles):
            return False
        else:
            for idx in range(len(self.titles)):
                if self.titles[idx] not in row[idx]:
                    return False
            return True

    def locate_begin_pos(self):
        line_num = 0

        for row in self.rows:
            # title的下一行 ，才是数据开始的行数
            line_num += 1
            if self.is_title_row(row):
                self.start = line_num
                return
        self.start = -1

    def locate_finish_pos(self):
        for idx in range(self.start, len(self.rows)):
            if len(self.rows[idx]) < len(self.titles):
                self.end = idx
                break

        if -1 == self.end:
            self.end = len(self.rows)

    def to_model(self, row):
        raise NotImplementedError

    def read(self):

        self.locate_begin_pos()
        self.locate_finish_pos()

        bills = []

        if self.start != -1 and self.end != -1:

            for idx in range(self.start, self.end):
                bill = self.to_model(self.rows[idx])
                bills.append(bill)

        bills.reverse()
        return bills
