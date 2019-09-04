# /usr/bin/python3


class Usuario():

    def __init__(self, ttask):
        self.ttask = ttask

    def finished(self):
        return self.ttask == 0

    def decrement(self):
        self.ttask -= 1

