# Generated by Django 3.2.4 on 2021-09-08 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_task_labels'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='executer',
            new_name='executor',
        ),
    ]