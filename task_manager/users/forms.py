from task_manager.users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2'
        ]
