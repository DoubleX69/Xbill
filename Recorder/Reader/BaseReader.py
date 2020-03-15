class BaseReader(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def is_standard_file(self, row=None):
        pass

    def read_line(self, row=None):
        pass

    def read(self):
        pass
