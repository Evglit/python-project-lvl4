from django.test import TestCase
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_users = 2
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_statuses = 1
        for status_num in range(number_of_statuses):
            Status.objects.create(name=f'Status {status_num}')

        number_of_tasks = 1
        for task_num in range(number_of_tasks):
            Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )

    def test_name_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Имя')
        field_label = task._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')
        field_label = task._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'Статус')
        field_label = task._meta.get_field('executer').verbose_name
        self.assertEquals(field_label, 'Исполнитель')
        field_label = task._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Автор')

    def test_name_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name(self):
        task = Task.objects.get(id=1)
        expected_object_name = task.name
        self.assertEquals(expected_object_name, str(task))
