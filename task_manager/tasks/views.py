from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_filters.views import FilterView
from task_manager.tasks.filters import TaskFilter
from task_manager.users.views import LOGIN_URL_NAME
from .models import Task
from .forms import TaskForm


TASKS_URL_NAME = reverse_lazy('tasks')


class TaskListPage(LoginRequiredMixin, FilterView):
    """Class for creating a task list page with filter."""
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks.html'
    login_url = LOGIN_URL_NAME
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class TaskDetailPage(LoginRequiredMixin, DetailView):
    """Class for creating a task detail page."""
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
    login_url = LOGIN_URL_NAME
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Task create class."""
    form_class = TaskForm
    template_name = 'form_create_task.html'
    success_url = TASKS_URL_NAME
    login_url = LOGIN_URL_NAME
    success_message = gettext('Задача успешно создана')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateTask, self).form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Task update class."""
    model = Task
    form_class = TaskForm
    template_name = 'form_update_task.html'
    success_url = TASKS_URL_NAME
    login_url = LOGIN_URL_NAME
    success_message = gettext('Задача успешно изменена')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class DeleteTask(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    "Task delete class"
    model = Task
    template_name = 'delete_task.html'
    success_url = TASKS_URL_NAME
    login_url = LOGIN_URL_NAME
    success_message = gettext('Задача успешно удалена')
    error_message = gettext('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object().name
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteTask, self).delete(request, *args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_authenticated and \
                obj.author.pk != self.request.user.pk:
            self.error_message = gettext('Задачу может удалить только её автор')
            self.login_url = TASKS_URL_NAME
            return False
        return True

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)
