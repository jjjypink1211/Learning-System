# Generated by Django 3.2.8 on 2022-03-21 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0022_remove_task_sub_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='sub_id',
            field=models.CharField(default=0, max_length=16, verbose_name='父任务编号'),
            preserve_default=False,
        ),
    ]
