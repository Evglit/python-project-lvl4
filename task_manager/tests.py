from django.urls import reverse
from django.test import TestCase
from task_manager.users.models import CustomUser


HOME_URL_NAME = reverse('home')
LOGIN_URL_NAME = reverse('login')
LOGOUT_URL_NAME = reverse('logout')


class HomeViewTest(TestCase):

    def test_view_uses_correct_template(self):
        response = self.client.get(HOME_URL_NAME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class LoginLogoutViewTest(TestCase):

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
        response = self.client.get(LOGIN_URL_NAME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_login.html')

    def test_login_logout(self):
        response = self.client.post(
            LOGIN_URL_NAME,
            {'username': 'Username 0', 'password': '123'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, HOME_URL_NAME)

        response = self.client.get(HOME_URL_NAME)
        self.assertEqual(str(response.context['user']), 'Username 0')

        response = self.client.post(LOGOUT_URL_NAME)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, HOME_URL_NAME)

        response = self.client.get(HOME_URL_NAME)
        self.assertEqual(str(response.context['user']), 'AnonymousUser')
