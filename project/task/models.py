from __future__ import unicode_literals
from datetime import date

from django.contrib.auth.models import User
from django.db import models


class TaskManager(models.Manager):
    def today(self):
        pass


class Task(models.Model):
    objects = TaskManager()
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='task_user')
    added_at = models.DateTimeField(auto_now_add=True)
    estimate = models.DateField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return '[{}] {}\n'.format(self.estimate, self.title).encode('utf8')

    def is_failed(self):
        return not self.is_done and self.estimate < date.today()