from django.test import TestCase
from task_manager.labels.models import Label


class LabelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Label.objects.create(name='Разное')

    def test_name_label(self):
        label = Label.objects.get(id=1)
        field_label = label._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Имя')

    def test_name_max_length(self):
        label = Label.objects.get(id=1)
        max_length = label._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name(self):
        label = Label.objects.get(id=1)
        expected_object_name = label.name
        self.assertEquals(expected_object_name, str(label))
