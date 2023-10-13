class A:
    attr = 0

    def __init__(self):
        self.attr = 1


class B:

    def __init__(self, a: A):
        self.a = a

    def change_a(self):
        self.a.attr = 2


a = A()

print(a.attr)

b = B(a)

b.change_a()

print(a.attr)