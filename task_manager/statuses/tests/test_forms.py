from django.test import TestCase
from task_manager.statuses.forms import StatusForm


class StatusFormTest(TestCase):

    def test_name_label(self):
        form = StatusForm()
        self.assertTrue(form.fields['name'].label == 'Имя')
