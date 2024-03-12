class LimitedException(Exception):
    def __init__(self, message):
        self.message = message

class NotEnoughTimeException(Exception):
    def __init__(self, message):
        self.message = message