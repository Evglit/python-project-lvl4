from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


HOME_URL_NAME = reverse_lazy('home')


class HomePage(TemplateView):
    """Class for creating a home page."""
    template_name = 'home.html'


class LoginUser(SuccessMessageMixin, LoginView):
    """CustomUser login class."""
    form_class = AuthenticationForm
    template_name = 'form_login.html'
    success_message = gettext('Вы залогинены')

    def get_success_url(seld):
        return HOME_URL_NAME


class LogoutUser(SuccessMessageMixin, LogoutView):
    """CustomUser Logout class."""
    next_page = HOME_URL_NAME
    success_message = gettext('Вы разлогинены')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, self.success_message)
        return response
