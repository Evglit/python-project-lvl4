from task_manager.labels.models import Label
from .models import Task
import django_filters
from django.forms.widgets import CheckboxInput


class TaskFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(
        label='Только свои задачи',
        method='my_tasks',
        widget=CheckboxInput
    )
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all(), label='Метка')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user.pk)
        return queryset
