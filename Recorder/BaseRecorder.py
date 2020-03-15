class BaseRecorder(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def save(self):
        raise NotImplementedError

    def update_same_xbill(self, xbill, same_xbills):
        raise NotImplementedError
