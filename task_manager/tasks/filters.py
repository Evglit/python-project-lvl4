from task_manager.labels.models import Label
from .models import Task
import django_filters
from django.forms.widgets import CheckboxInput
from django.utils.translation import gettext


class TaskFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(
        label=gettext('Только свои задачи'),
        method='my_tasks',
        widget=CheckboxInput
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=gettext('Метка')
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user.pk)
        return queryset
