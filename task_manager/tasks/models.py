from django.db import models
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser
from task_manager.labels.models import Label
from django.utils.translation import gettext


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name=gettext('Имя'))
    description = models.TextField(
        verbose_name=gettext('Описание'),
        blank=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=gettext('Статус'),
    )
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name=gettext('Исполнитель'),
        related_name='executor',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name=gettext('Автор'),
        related_name='author'
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name=gettext('Метки'),
        blank=True
    )
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
