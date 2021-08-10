from django.test import TestCase
from task_manager.statuses.models import Statuses
from django.contrib.auth.models import User
from django.urls import reverse


class StatusListViewTest(TestCase):

    def setUp(self):
        number_of_users = 1
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_statuses = 5
        for status_num in range(number_of_statuses):
            Statuses.objects.create(name=f'Status {status_num}')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('statuses'))
        self.assertRedirects(response, '/login/?next=/statuses/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse('statuses'))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses.html')
        self.assertTrue(len(response.context['statuses']) == 5)


class CreateStatusViewTest(TestCase):

    def setUp(self):
        number_of_users = 1
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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create_status'))
        self.assertRedirects(response, '/login/?next=/statuses/create/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse('create_status'))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        
    def test_create(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(reverse('create_status'), {'name': 'Creation test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/statuses/')
        self.assertTrue(Statuses.objects.get(name='Creation test'))


class UpdateStatusViewTest(TestCase):
    
    def setUp(self):
        number_of_users = 1
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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('update_status', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse('update_status', kwargs={'pk':1}))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_update(self):
        new_name = 'Updation test'
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse('update_status', kwargs={'pk':1}),
            {'name':new_name}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('statuses')))
        self.assertEqual(Statuses.objects.get(pk=1).name, new_name)


class DeleteStatusViewTest(TestCase):

    def setUp(self):
        number_of_users = 1
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_statuses = 2
        for status_num in range(number_of_statuses):
            Statuses.objects.create(name=f'Status {status_num}')
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('delete_status', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse('delete_status', kwargs={'pk':1}))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete.html')
    
    def test_delete(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(reverse('delete_status', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('statuses')))
        self.assertFalse(Statuses.objects.filter(pk=1))
