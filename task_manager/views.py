from django.views.generic.base import TemplateView
from django.utils.translation import gettext


class HomePage(TemplateView):

    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('')
        return context


class UserPage(TemplateView):

    template_name = 'users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Пользователи')
        return context


class LoginPage(TemplateView):

    template_name = 'login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Вход')
        return context


class CreatePage(TemplateView):

    template_name = 'create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = gettext('Регистрация')
        return context
