from django.db import models
from task_manager.statuses.models import Statuses
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT, verbose_name='Статус')
    executer = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Исполнитель')
    author = models.CharField(max_length=100, verbose_name='Автор')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
