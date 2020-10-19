from django.test import TestCase

# Create your tests here.

class prototest(object):
    def __init__(self, r, m):
        self.m = m
        self.r = r

    @property
    def t(self):
        return self.m

    @classmethod
    def y(cls, m):
        cls.m = m
        print("oko %s" % m)

p = prototest('r', 'm')
print(p.t)
u = prototest.y('xxx')
print(u.t)
