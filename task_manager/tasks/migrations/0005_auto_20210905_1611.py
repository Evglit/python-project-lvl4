# Generated by Django 3.2.4 on 2021-09-05 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0003_alter_label_name'),
        ('tasks', '0004_auto_20210823_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, to='labels.Label', verbose_name='Метки'),
        ),
    ]
