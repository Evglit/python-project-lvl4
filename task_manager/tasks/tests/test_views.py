from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.views import LOGIN_URL_NAME, FORM_HTML, DELETE_HTML
from task_manager.tasks.views import TASKS_URL_NAME


TAKS_DETAIL_URL_NAME = 'task_detail'
CREATE_TASK_URL_NAME = 'create_task'
UPDATE_TASK_URL_NAME = 'update_task'
DELETE_TASK_URL_NAME = 'delete_task'


class TaskListViewTest(TestCase):

    def setUp(self):
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

        number_of_labels = 1
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')

        number_of_tasks = 5
        for task_num in range(number_of_tasks):
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )
            a.labels.add(Label.objects.get(pk=1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(TASKS_URL_NAME ))
        self.assertRedirects(response, reverse(LOGIN_URL_NAME))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(TASKS_URL_NAME ))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')
        self.assertTrue(len(response.context['tasks']) == 5)


class TaskDetailViewTest(TestCase):

    def setUp(self):
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

        number_of_labels = 1
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')

        number_of_tasks = 1
        for task_num in range(number_of_tasks):
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )
            a.labels.add(Label.objects.get(pk=1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(TASKS_URL_NAME ))
        self.assertRedirects(response, reverse(LOGIN_URL_NAME))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(TAKS_DETAIL_URL_NAME, kwargs={'pk':1}))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_detail.html')


class CreateTaskViewTest(TestCase):

    def setUp(self):
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

        number_of_labels = 1
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')
        
        number_of_tasks = 2
        for task_num in range(number_of_tasks):
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )
            a.labels.add(Label.objects.get(pk=1))
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(CREATE_TASK_URL_NAME))
        self.assertRedirects(response, reverse(LOGIN_URL_NAME))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(CREATE_TASK_URL_NAME))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, FORM_HTML)

    def test_create(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(CREATE_TASK_URL_NAME),
                {
                    'name': 'Task creation test',
                    'description': 'Task creation test',
                    'status': 1,
                    'executer': 2,
                    'labels': 1
                }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(TASKS_URL_NAME))
        self.assertTrue(Task.objects.get(name='Task creation test'))
        response = self.client.get(reverse(TASKS_URL_NAME ))
        self.assertEqual(response.context['user'], Task.objects.get(name='Task creation test').author)


class UpdateTaskViewTest(TestCase):

    def setUp(self):
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

        number_of_labels = 1
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')
        
        number_of_tasks = 1
        for task_num in range(number_of_tasks):
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )
            a.labels.add(Label.objects.get(pk=1))
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(UPDATE_TASK_URL_NAME, kwargs={'pk':1}))
        self.assertRedirects(response, reverse(LOGIN_URL_NAME))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(UPDATE_TASK_URL_NAME, kwargs={'pk':1}))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, FORM_HTML)

    def test_update(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(UPDATE_TASK_URL_NAME, kwargs={'pk':1}),
                {
                    'name': 'Task update test',
                    'description': 'Task update test',
                    'status': 1,
                    'executer': 2,
                    'labels': 1
                }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(TASKS_URL_NAME)))
        self.assertTrue(Task.objects.get(name='Task update test'))


class DeleteTaskViewTest(TestCase):

    def setUp(self):
        number_of_users = 3
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

        number_of_labels = 1
        for labels_num in range(number_of_labels):
            Label.objects.create(name=f'Label {labels_num}')
        
        number_of_tasks = 2
        for task_num in range(number_of_tasks):
            a = Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Status.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )
            a.labels.add(Label.objects.get(pk=1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(DELETE_TASK_URL_NAME, kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(LOGIN_URL_NAME)))

    def test_redirect_if_logged_in_but_not_passed_test(self):
        self.client.login(username='Username 1', password='123')
        response = self.client.get(reverse(DELETE_TASK_URL_NAME, kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(TASKS_URL_NAME)))

    def test_logged_in_passed_test_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(DELETE_TASK_URL_NAME, kwargs={'pk':1}))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, DELETE_HTML)

    def test_delete(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(reverse(DELETE_TASK_URL_NAME, kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(TASKS_URL_NAME)))
        self.assertFalse(Task.objects.filter(pk=1))
