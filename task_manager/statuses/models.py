from django.db import models
from django.utils.translation import gettext


class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name=gettext('Имя'))
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
