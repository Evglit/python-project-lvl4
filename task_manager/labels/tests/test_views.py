from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from task_manager.users.views import LOGIN_URL_NAME, FORM_HTML, DELETE_HTML
from task_manager.labels.views import LABELS_URL_NAME


CREATE_LABEL_URL_NAME = 'create_label'
UPDATE_LABEL_URL_NAME = 'update_label'
DELETE_LABEL_URL_NAME = 'delete_label'


class TestListLabelView(TestCase):

    def setUp(self):
        number_of_users = 1
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_label = 5
        for label_num in range(number_of_label):
            Label.objects.create(name=f'Label {label_num}')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(LABELS_URL_NAME))
        self.assertRedirects(response, reverse(LOGIN_URL_NAME))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(LABELS_URL_NAME))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels.html')
        self.assertTrue(len(response.context[LABELS_URL_NAME]) == 5)


class CreateLabelViewTest(TestCase):

    def setUp(self):
        number_of_users = 1
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_label = 1
        for label_num in range(number_of_label):
            Label.objects.create(name=f'Label {label_num}')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(CREATE_LABEL_URL_NAME))
        self.assertRedirects(response, reverse(LOGIN_URL_NAME))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(reverse(CREATE_LABEL_URL_NAME))
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, FORM_HTML)

    def test_create(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(CREATE_LABEL_URL_NAME),
            {'name': 'Creation test'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LABELS_URL_NAME))
        self.assertTrue(Label.objects.get(name='Creation test'))


class UpdateLabelViewTest(TestCase):

    def setUp(self):
        number_of_users = 1
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_label = 1
        for label_num in range(number_of_label):
            Label.objects.create(name=f'Label {label_num}')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(UPDATE_LABEL_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(LOGIN_URL_NAME)))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(
            reverse(UPDATE_LABEL_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(str(response.context['user']), 'Username 0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, FORM_HTML)

    def test_update(self):
        new_name = 'Updation test'
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(UPDATE_LABEL_URL_NAME, kwargs={'pk': 1}),
            {'name': new_name}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(LABELS_URL_NAME)))
        self.assertEqual(Label.objects.get(pk=1).name, new_name)


class DeleteLabelViewTest(TestCase):

    def setUp(self):
        number_of_users = 1
        for user_num in range(number_of_users):
            User.objects.create_user(
                first_name=f'First name {user_num}',
                last_name=f'Last name {user_num}',
                username=f'Username {user_num}',
                password='123',
            )

        number_of_label = 2
        for label_num in range(number_of_label):
            Label.objects.create(name=f'Label {label_num}')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(DELETE_LABEL_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(LOGIN_URL_NAME)))

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.get(
            reverse(DELETE_LABEL_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(
            str(response.context['user']),
            'Username 0'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, DELETE_HTML)

    def test_delete(self):
        self.client.login(username='Username 0', password='123')
        response = self.client.post(
            reverse(DELETE_LABEL_URL_NAME, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse(LABELS_URL_NAME)))
        self.assertFalse(Label.objects.filter(pk=1))
