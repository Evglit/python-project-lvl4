from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from task_manager.users.views import LOGIN_URL_NAME, FORM_HTML, DELETE_HTML
from .models import Task
from .forms import TaskForm


TASKS_URL_NAME = 'tasks'


class TaskListPage(LoginRequiredMixin, ListView):
    """Class for creating a task list page."""
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy(LOGIN_URL_NAME)
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Задачи'
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class TaskDetailPage(LoginRequiredMixin, DetailView):
    """Class for creating a task detail page."""
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy(LOGIN_URL_NAME)
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.get_object())
        context['title'] = 'Просмотр задачи'
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Task create class."""
    form_class = TaskForm
    template_name = FORM_HTML
    success_url = reverse_lazy(TASKS_URL_NAME)
    login_url = reverse_lazy(LOGIN_URL_NAME)
    success_message = 'Статус успешно создан'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать задачу'
        context['command'] = 'Создать'
        return context

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
    template_name = FORM_HTML
    success_url = reverse_lazy(TASKS_URL_NAME)
    login_url = reverse_lazy(LOGIN_URL_NAME)
    success_massage = 'Задача успешно изменена'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение задачи'
        context['command'] = 'Изменить'
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class DeleteTask(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    "Task delete class"
    model = Task
    template_name = DELETE_HTML
    success_url = reverse_lazy(TASKS_URL_NAME)
    login_url = reverse_lazy(LOGIN_URL_NAME)
    success_message = 'Задача успешно удалена'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление задачу'
        context['command'] = 'Да, удалить'
        context['object'] = self.get_object().name
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteTask, self).delete(request, *args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        return str(obj.author) == str(self.request.user)
    
    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_authenticated and obj.author != self.request.user.username:
            self.error_message = 'Задачу может удалить только её автор'
            self.login_url = reverse_lazy(TASKS_URL_NAME)
            return False
        return True

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)
