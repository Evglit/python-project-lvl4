from django.db import models
from django.urls import reverse


class Users(models.Model):
    id_first_name = models.CharField(max_length=255)
    id_last_name = models.CharField(max_length=255)
    id_username = models.CharField(max_length=255)
    id_password1 = models.CharField(max_length=255)
    id_password2 = models.CharField(max_length=255)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-create"]

    def __str__(self):
        return self.id_username
