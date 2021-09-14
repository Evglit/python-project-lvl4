from django.urls import reverse
from django.test import TestCase
from task_manager.users.models import CustomUser
from task_manager.tests import LOGIN_URL_NAME


USERS_URL_NAME = reverse('users')
CREATE_USER_URL_NAME = reverse('create_user')
UPDATE_USER_URL_NAME = 'update_user'
DELETE_USER_URL_NAME = 'delete_user'


class UserListViewTest(TestCase):

    @classmethod
    def setUpTestData(cla):
        number_of_users = 5
        for user_num in range(number_of_users):
            CustomUser.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123'
            )

    def test_view_uses_correct_template(self):
        response = self.client.get(USERS_URL_NAME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')

    def test_lists_all_users(self):
        response = self.client.get(USERS_URL_NAME)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['users']) == 5)


class CreateUserViewTest(TestCase):

    def setUp(self):
        number_of_users = 1
        for user_num in range(number_of_users):
            CustomUser.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

    def test_view_uses_correct_template(self):
        response = self.client.get(CREATE_USER_URL_NAME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_create_user.html')

    def test_create(self):
        response = self.client.post(
            CREATE_USER_URL_NAME,
            {
                'first_name': 'test',
                'last_name': 'create',
                'username': 'test_create',
                'password1': '123',
                'password2': '123',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, LOGIN_URL_NAME)
        self.assertTrue(CustomUser.objects.get(username='test_create'))


class UpdateUserViewTest(TestCase):

    def setUp(self):
        number_of_users = 2
        for user_num in range(number_of_users):
            CustomUser.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(UPDATE_USER_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL_NAME))

    def test_redirect_if_logged_in_but_not_passed_test(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(
            reverse(UPDATE_USER_URL_NAME, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(USERS_URL_NAME))

    def test_logged_in_passed_test_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(
            reverse(UPDATE_USER_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_update_user.html')

    def test_update(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(UPDATE_USER_URL_NAME, kwargs={'pk': 1}),
            {
                'first_name': 'test',
                'last_name': 'update',
                'username': 'test_update',
                'password1': '123',
                'password2': '123',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(USERS_URL_NAME))
        self.assertEqual(CustomUser.objects.get(pk=1).username, 'test_update')


class DeleteUserViewTest(TestCase):

    def setUp(self):
        number_of_users = 2
        for user_num in range(number_of_users):
            CustomUser.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(DELETE_USER_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL_NAME))

    def test_redirect_if_logged_in_but_not_passed_test(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(
            reverse(DELETE_USER_URL_NAME, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(USERS_URL_NAME))

    def test_logged_in_passed_test_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(
            reverse(DELETE_USER_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_user.html')

    def test_delete(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(DELETE_USER_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(USERS_URL_NAME))
        self.assertFalse(CustomUser.objects.filter(pk=1))
