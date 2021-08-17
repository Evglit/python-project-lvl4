from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


URL_USERS = 'users'
URL_HOME = 'home'
URL_LOGIN = 'login'
URL_LOGOUT = 'logout'
URL_CREATE_USER = 'create_user'
URL_UPDATE_USER = 'update_user'
URL_DELETE_USER = 'delete_user'
HTML_FORM = 'form.html'


class HomeViewTest(TestCase):

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(URL_HOME))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class UserListViewTest(TestCase):

    @classmethod
    def setUpTestData(cla):
        number_of_users = 5
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123'
            )

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(URL_USERS))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')

    def test_lists_all_users(self):
        response = self.client.get(reverse(URL_USERS))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['users']) == 5)


class LoginLogoutViewTest(TestCase):

    def setUp(self):
        number_of_users = 1
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(URL_LOGIN))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, HTML_FORM)
    
    def test_login_logout(self):
        response = self.client.post(reverse(URL_LOGIN), {'username':'Username 0', 'password':'123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(URL_HOME))

        response = self.client.get(reverse(URL_HOME))
        self.assertEqual(str(response.context['user']), 'Username 0')
        
        response = self.client.post(reverse(URL_LOGOUT))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(URL_HOME))
        
        response = self.client.get(reverse(URL_HOME))
        self.assertEqual(str(response.context['user']), 'AnonymousUser')


class CreateUserViewTest(TestCase):

    def setUp(self):
        number_of_users = 1
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(URL_CREATE_USER))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, HTML_FORM)

    def test_create(self):
        response = self.client.post(
            reverse(URL_CREATE_USER),
                {
                    'first_name': 'test',
                    'last_name': 'create',
                    'username': 'test_create',
                    'password1': '123',
                    'password2': '123',
                }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(URL_LOGIN))
        self.assertTrue(User.objects.get(username='test_create'))


class UpdateUserViewTest(TestCase):

    def setUp(self):
        number_of_users = 2
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(URL_UPDATE_USER, kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_LOGIN)))

    def test_redirect_if_logged_in_but_not_passed_test(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(URL_UPDATE_USER, kwargs={'pk':2}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_USERS)))

    def test_logged_in_passed_test_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(URL_UPDATE_USER, kwargs={'pk':1}))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_update(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(URL_UPDATE_USER, kwargs={'pk':1}),
                {
                    'first_name': 'test',
                    'last_name': 'update',
                    'username': 'test_update',
                    'password1': '123',
                    'password2': '123',
                }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_USERS)))
        self.assertEqual(User.objects.get(pk=1).username, 'test_update')


class DeleteUserViewTest(TestCase):

    def setUp(self):
        number_of_users = 2
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(URL_DELETE_USER, kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_LOGIN)))

    def test_redirect_if_logged_in_but_not_passed_test(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(URL_DELETE_USER, kwargs={'pk':2}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_USERS)))

    def test_logged_in_passed_test_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(URL_DELETE_USER, kwargs={'pk':1}))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete.html')

    def test_delete(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(reverse(URL_DELETE_USER, kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(URL_USERS)))
        self.assertFalse(User.objects.filter(pk=1))
