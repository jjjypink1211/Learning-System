# Generated by Django 3.2.8 on 2022-03-21 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0015_alter_task_sub_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='sub_id',
        ),
    ]
