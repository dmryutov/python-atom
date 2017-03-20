# -*- coding: utf-8 -*-
from datetime import date

class Task:
    def __init__(self, title, estimate, state='in_progress'):
        if state not in ('in_progress', 'ready'):
            raise AttributeError('State should be `in_progress` or `ready`!')
        self.title = title
        self.state = state
        self.estimate = estimate

    def __str__(self):
        return '[{}]({}) {}\n'.format(self.estimate, self.state, self.title)

    @property
    def remaining(self):
        return self.estimate - date.today() if self.state == 'in_progress' else 0

    @property
    def is_failed(self):
        return self.state == 'in_progress' and self.estimate < date.today()

    def ready(self):
        self.state = 'ready'


class Roadmap:
    def __init__(self, tasks=[]):
        self.tasks = tasks

    @property
    def today(self):
        return [i for i in self.tasks if i.estimate == date.today()]

    def filter(self, state):
        return [i for i in self.tasks if i.state == state]


r = Roadmap([
        Task('t1', date(2017, 10, 21)),
        Task('t2', date(2017, 2, 10), 'ready'),
        Task('t3', date(2017, 1, 10), 'in_progress'),
        Task('t4', date(2017, 3, 19)),
    ])

print('', *r.tasks)
for i in r.today:
    print(i.title, i.estimate, i.state, i.remaining, i.is_failed)