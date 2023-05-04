class AppException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class InvalidInputException(AppException):
    def __init__(self,msg):
        AppException.__init__(self,msg)