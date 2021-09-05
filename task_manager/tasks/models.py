from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус',
    )
    executer = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name='Исполнитель',
        related_name='executer'
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name='Автор',
        related_name='author'
    )
    labels = models.ManyToManyField(Label, verbose_name='Метки')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
