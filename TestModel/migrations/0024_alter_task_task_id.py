# Generated by Django 3.2.8 on 2022-03-27 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0023_task_sub_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_id',
            field=models.IntegerField(unique=True, verbose_name='任务编号'),
        ),
    ]