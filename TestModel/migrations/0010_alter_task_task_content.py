# Generated by Django 3.2.8 on 2022-01-12 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0009_task_task_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_content',
            field=models.CharField(max_length=255, verbose_name='任务内容'),
        ),
    ]