# -*- coding: utf-8 -*-
class Charge:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return round(self._value, 2)


class Account:
    def __init__(self, value = 0):
        self.charges = []
        self.total   = value

    def __iter__(self):
        yield from self.charges

    def income(self, value):
        if (value <= 0):
            raise Exception('Value should be greater than 0!')
        self.charges.append(Charge(value))
        self.total += self.charges[-1].value

    def outcome(self, value):
        if (value <= 0):
            raise Exception('Value should be greater than 0!')
        if (value > self.total):
            raise Exception('Insufficient funds on the account!')
        self.charges.append(Charge(-value))
        self.total += self.charges[-1].value


account = Account(50)
account.income(10.123)
account.outcome(3.461)
account.income(5.246)

print ('total value: %.2f' % account.total)
for i, acc in enumerate(account, 1):
    print('transaction %d: %.2f' % (i, acc.value))