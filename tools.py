class Ret(object):
    def __init__(self):
        self.code = 0
        self.msg = ""
        self.data = {}

    @property
    def dict(self):
        return self.__dict__
