from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect


class TaskListPage(LoginRequiredMixin, ListView):
    """Class for creating a tasks page."""
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Задачи'
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class TaskDetailPage(LoginRequiredMixin, DetailView):
    """Class for creating a tasks page."""
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Просмотр задачи'
        return context

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Task registration class."""
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
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
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
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
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
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
        if not self.request.user.is_authenticated:
            return False
        elif obj.pk != self.request.user.pk:
            self.error_message = 'У вас нет прав для изменения другого пользователя.'
            self.login_url = self.success_url
            return False
        return True

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.login_url)