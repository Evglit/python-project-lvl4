from django.test import TestCase
from task_manager.statuses.models import Status


class StatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='Просрочено')

    def test_name_label(self):
        status = Status.objects.get(id=1)
        field_label = status._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Имя')

    def test_name_max_length(self):
        status = Status.objects.get(id=1)
        max_length = status._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name(self):
        status = Status.objects.get(id=1)
        expected_object_name = status.name
        self.assertEquals(expected_object_name, str(status))
