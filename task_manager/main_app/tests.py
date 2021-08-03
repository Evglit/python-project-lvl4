from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


test_user = {
    'first_name': 'User2',
    'last_name': 'Test2',
    'username': 'TestUser2',
    'password1': '123',
    'password2': '123',
}

test_user_update = {
    'first_name': 'User_update',
    'last_name': 'Test_update',
    'username': 'TestUser_update',
    'password1': '123',
    'password2': '123',
}

login = {
    'username': 'User2',
    'password': '123',
}


class CrudTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create(
            first_name = 'User1',
            last_name = 'Test1',
            username = 'TestUser1',
            password = '123',
        )
        test_user1.save()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_users_page(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')

    def test_create_page(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/users/1/update/')
        self.assertRedirects(response, '/login/?next=/users/1/update/')
        response = self.client.get('/users/1/delete/')
        self.assertRedirects(response, '/login/?next=/users/1/delete/')


    def test_create_user(self):
        response = self.client.post(reverse('create'), test_user)
        print(User.objects.get(pk=2).username)
        self.assertEqual(response.status_code, 302)


    def test_login_user(self):
        print(User.objects.get(pk=1).username)
        login = self.client.login(username='TestUser1', password='123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'TestUser1')
        #self.assertTrue(self.request.user.is_authenticated)
        #response = self.client.get('/users/1/update/')
        #print(User.objects.get(pk=1).username)

'''
    def test_login_page(self):
        response = self.client.get('/users/2/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_update_user(self):
        response = self.client.post('/users/2/update/', test_user_update)
        print(User.objects.get(pk=2))
        self.assertEqual(response.status_code, 302)
'''