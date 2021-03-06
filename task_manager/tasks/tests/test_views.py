from django.urls import reverse
from django.test import TestCase
from task_manager.users.models import CustomUser
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.tests import LOGIN_URL_NAME


TASKS_URL_NAME = reverse('tasks')
CREATE_TASK_URL_NAME = reverse('create_task')
TAKS_DETAIL_URL_NAME = 'task_detail'
UPDATE_TASK_URL_NAME = 'update_task'
DELETE_TASK_URL_NAME = 'delete_task'


class TaskListViewTest(TestCase):

    def setUp(self):
        number_of_users = 2
        for user_num in range(number_of_users):
            CustomUser.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_statuses = 2
        for status_num in range(number_of_statuses):
            Status.objects.create(name=f'Status {status_num}')

        number_of_labels = 2
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')

        number_of_tasks = 5
        for task_num in range(number_of_tasks):
            num1 = 1 if task_num < 3 else 2
            num2 = 2 if task_num < 3 else 1
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=num1),
                executor=CustomUser.objects.get(pk=num2),
                author=CustomUser.objects.get(pk=num1)
            )
            a.labels.add(Label.objects.get(pk=num1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(TASKS_URL_NAME)
        self.assertRedirects(response, LOGIN_URL_NAME)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(TASKS_URL_NAME)
        self.assertEqual(
            str(response.context['user']),
            'First name 0 Last name 0'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')
        self.assertTrue(len(response.context['filter'].qs) == 5)

    def test_filter(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(TASKS_URL_NAME, {'executor': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['filter'].qs), 2)
        response = self.client.get(
            TASKS_URL_NAME,
            {'self_tasks': 'on'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['filter'].qs), 3)
        response = self.client.get(TASKS_URL_NAME, {'status': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['filter'].qs), 3)
        response = self.client.get(TASKS_URL_NAME, {'labels': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['filter'].qs), 2)


class TaskDetailViewTest(TestCase):

    def setUp(self):
        number_of_users = 2
        for user_num in range(number_of_users):
            CustomUser.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_statuses = 1
        for status_num in range(number_of_statuses):
            Status.objects.create(name=f'Status {status_num}')

        number_of_labels = 1
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')

        number_of_tasks = 1
        for task_num in range(number_of_tasks):
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executor=CustomUser.objects.get(pk=2),
                author=CustomUser.objects.get(pk=1)
            )
            a.labels.add(Label.objects.get(pk=1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(TASKS_URL_NAME)
        self.assertRedirects(response, LOGIN_URL_NAME)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(
            reverse(TAKS_DETAIL_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(
            str(response.context['user']),
            'First name 0 Last name 0'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_detail.html')


class CreateTaskViewTest(TestCase):

    def setUp(self):
        number_of_users = 2
        for user_num in range(number_of_users):
            CustomUser.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_statuses = 1
        for status_num in range(number_of_statuses):
            Status.objects.create(name=f'Status {status_num}')

        number_of_labels = 1
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')

        number_of_tasks = 2
        for task_num in range(number_of_tasks):
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executor=CustomUser.objects.get(pk=2),
                author=CustomUser.objects.get(pk=1)
            )
            a.labels.add(Label.objects.get(pk=1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(CREATE_TASK_URL_NAME)
        self.assertRedirects(response, LOGIN_URL_NAME)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(CREATE_TASK_URL_NAME)
        self.assertEqual(
            str(response.context['user']),
            'First name 0 Last name 0'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_create_task.html')

    def test_create(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            CREATE_TASK_URL_NAME,
            {
                'name': 'Task creation test',
                'description': 'Task creation test',
                'status': 1,
                'executor': 2,
                'labels': 1
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TASKS_URL_NAME)
        self.assertTrue(Task.objects.get(name='Task creation test'))
        response = self.client.get(TASKS_URL_NAME)
        self.assertEqual(
            response.context['user'],
            Task.objects.get(name='Task creation test').author
        )


class UpdateTaskViewTest(TestCase):

    def setUp(self):
        number_of_users = 2
        for user_num in range(number_of_users):
            CustomUser.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_statuses = 1
        for status_num in range(number_of_statuses):
            Status.objects.create(name=f'Status {status_num}')

        number_of_labels = 1
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')

        number_of_tasks = 1
        for task_num in range(number_of_tasks):
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executor=CustomUser.objects.get(pk=2),
                author=CustomUser.objects.get(pk=1)
            )
            a.labels.add(Label.objects.get(pk=1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(UPDATE_TASK_URL_NAME, kwargs={'pk': 1})
        )
        self.assertRedirects(response, LOGIN_URL_NAME)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(
            reverse(UPDATE_TASK_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(
            str(response.context['user']),
            'First name 0 Last name 0'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_update_task.html')

    def test_update(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(UPDATE_TASK_URL_NAME, kwargs={'pk': 1}),
            {
                'name': 'Task update test',
                'description': 'Task update test',
                'status': 1,
                'executor': 2,
                'labels': 1
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(TASKS_URL_NAME))
        self.assertTrue(Task.objects.get(name='Task update test'))


class DeleteTaskViewTest(TestCase):

    def setUp(self):
        number_of_users = 3
        for user_num in range(number_of_users):
            CustomUser.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_statuses = 1
        for status_num in range(number_of_statuses):
            Status.objects.create(name=f'Status {status_num}')

        number_of_labels = 1
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')

        number_of_tasks = 2
        for task_num in range(number_of_tasks):
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executor=CustomUser.objects.get(pk=2),
                author=CustomUser.objects.get(pk=1)
            )
            a.labels.add(Label.objects.get(pk=1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(DELETE_TASK_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL_NAME))

    def test_redirect_if_logged_in_but_not_passed_test(self):
        self.client.login(username='Username 1', password='123')
        response = self.client.get(
            reverse(DELETE_TASK_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(TASKS_URL_NAME))

    def test_logged_in_passed_test_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(
            reverse(DELETE_TASK_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(
            str(response.context['user']),
            'First name 0 Last name 0'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_task.html')

    def test_delete(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(DELETE_TASK_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(TASKS_URL_NAME))
        self.assertFalse(Task.objects.filter(pk=1))
