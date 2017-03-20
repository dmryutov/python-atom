# -*- coding: utf-8 -*-
from datetime import date

from parse import get_dataset

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

    @property
    def critical(self):
        return [i for i in self.tasks if (i.estimate - date.today()).days < 3 and
                                            i.state == 'in_progress']

    def filter(self, state):
        return [i for i in self.tasks if i.state == state]

    def loadTasks(self):
        for rec in get_dataset('dataset.yml'):
            self.tasks.append(Task(rec[0], rec[2], rec[1]))