# Generated by Django 3.2.8 on 2022-03-13 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0010_alter_task_task_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='learn_obj',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('obj_content', models.CharField(max_length=255, verbose_name='目标内容')),
                ('obj_time', models.DateTimeField(auto_now_add=True, verbose_name='目标时间')),
                ('obj_author', models.CharField(max_length=16, verbose_name='作者')),
                ('obj_type', models.CharField(choices=[(1, '总教学目标'), (2, '小组教学目标')], max_length=2, verbose_name='目标类型')),
            ],
        ),
    ]
