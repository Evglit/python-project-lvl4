from django.test import TestCase
from task_manager.labels.forms import LabelForm


class LabelFormTest(TestCase):

    def test_name_label(self):
        form = LabelForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'Имя')
