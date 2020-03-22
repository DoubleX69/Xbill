class BaseRecorder(object):

    def __init__(self, rows):
        self.rows = rows

    def save(self):
        raise NotImplementedError

    def update_same_xbill(self, xbill, same_xbills):
        raise NotImplementedError
