from django.test import TestCase
from task_manager.tasks.models import Task
from task_manager.statuses.models import Statuses
from django.contrib.auth.models import User
from django.urls import reverse


URL_LOGIN = 'login'
URL_TASKS = 'tasks'
URL_TAKS_DETAIL = 'task_detail'
URL_CREATE_TASK = 'create_task'
URL_UPDATE_TASK = 'update_task'
URL_DELETE_TASK = 'delete_task'
HTML_FORM = 'form.html'


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
            Statuses.objects.create(name=f'Status {status_num}')
        
        number_of_tasks = 5
        for task_num in range(number_of_tasks):
            Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Statuses.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(URL_TASKS ))
        self.assertRedirects(response, reverse(URL_LOGIN))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(URL_TASKS ))
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
            Statuses.objects.create(name=f'Status {status_num}')
        
        number_of_tasks = 1
        for task_num in range(number_of_tasks):
            Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Statuses.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(URL_TASKS ))
        self.assertRedirects(response, reverse(URL_LOGIN))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(URL_TAKS_DETAIL, kwargs={'pk':1}))
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
            Statuses.objects.create(name=f'Status {status_num}')
        
        number_of_tasks = 2
        for task_num in range(number_of_tasks):
            Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Statuses.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(URL_CREATE_TASK))
        self.assertRedirects(response, reverse(URL_LOGIN))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(URL_CREATE_TASK))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, HTML_FORM)

    def test_create(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(URL_CREATE_TASK),
                {
                    'name': 'Task creation test',
                    'description': 'Task creation test',
                    'status': Statuses.objects.get(pk=1),
                    'executer': User.objects.get(pk=2),
                }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(URL_TASKS))
        self.assertTrue(Task.objects.get(name='Task creation test'))
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
            Statuses.objects.create(name=f'Status {status_num}')
        
        number_of_tasks = 1
        for task_num in range(number_of_tasks):
            Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Statuses.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(URL_UPDATE_TASK, kwargs={'pk':1}))
        self.assertRedirects(response, reverse(URL_LOGIN))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(URL_UPDATE_TASK, kwargs={'pk':1}))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, HTML_FORM)

    def test_update(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(URL_UPDATE_TASK, kwargs={'pk':1}),
                {
                    'name': 'Task update test',
                    'description': 'Task update test',
                    'status': Statuses.objects.get(pk=1),
                    'executer': User.objects.get(pk=2),
                }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_TASKS)))
        self.assertTrue(Task.objects.get(name='Task update test'))


class DeleteTaskViewTest(TestCase):

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
            Statuses.objects.create(name=f'Status {status_num}')
        
        number_of_tasks = 2
        for task_num in range(number_of_tasks):
            Task.objects.create(
                name=f'Task {task_num}',
                description=f'Task description {task_num}',
                status=Statuses.objects.get(pk=1),
                executer=User.objects.get(pk=2),
                author=User.objects.get(pk=1)
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(URL_DELETE_TASK, kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_LOGIN)))

    def test_redirect_if_logged_in_but_not_passed_test(self):
        self.client.login(username='Username 1', password='123')
        response = self.client.get(reverse(URL_DELETE_TASK, kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_TASKS)))

    def test_logged_in_passed_test_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(URL_DELETE_TASK, kwargs={'pk':1}))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete.html')

    def test_delete(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(reverse(URL_DELETE_TASK, kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_TASKS)))
        self.assertFalse(Task.objects.filter(pk=1))
