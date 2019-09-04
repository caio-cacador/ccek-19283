# /usr/bin/python3


class Servidor():

    def __init__(self, umax):
        self.usuarios = []
        self.custo = 0
        self.umax = umax

    def is_empty(self):
        return len(self.usuarios) == 0

    def is_full(self):
        return len(self.usuarios) == self.umax

    def update(self):
        self.custo += 1
        for __usuario in self.usuarios:
            __usuario.decrement()

    def getTotalTtask(self):
        total = 0
        for user in self.usuarios:
            total += user.ttask
        return total
