from django.test import TestCase
from task_manager.statuses.forms import CreateStatusForm


class StatusFormTest(TestCase):

    def test_name_label(self):
        form = CreateStatusForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'Имя')
