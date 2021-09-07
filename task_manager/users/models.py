from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def __str__(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name
