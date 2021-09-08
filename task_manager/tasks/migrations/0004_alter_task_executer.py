# Generated by Django 3.2.4 on 2021-09-08 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0003_alter_task_executer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='executer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='executer', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
    ]
