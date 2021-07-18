from task_manager.main_app.models import Users
from django import forms
from django.utils.translation import gettext


class CreateUserForm(forms.ModelForm):
    id_first_name = forms.CharField(max_length=255, label=gettext("Имя"))
    id_last_name = forms.CharField(max_length=255, label=gettext("Фамилия"))
    id_username = forms.CharField(max_length=255, label=gettext("Имя пользователя"), help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.')
    id_password1 = forms.CharField(max_length=255, label=gettext("Пароль"), help_text='Ваш пароль должен содержать как минимум 3 символа.')
    id_password2 = forms.CharField(max_length=255, label=gettext("Подтверждение пароля"), help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.')

    class Meta:
        model = Users
        fields = ['id_first_name', 'id_last_name', 'id_username',
                    'id_password1', 'id_password2']
