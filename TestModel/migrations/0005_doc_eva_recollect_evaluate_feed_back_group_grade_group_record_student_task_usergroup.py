# Generated by Django 3.2.8 on 2021-12-20 15:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0004_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='doc',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group_id', models.IntegerField(unique=True, verbose_name='小组编号')),
                ('num', models.CharField(max_length=11, unique=True, verbose_name='学生学号')),
                ('task_id', models.CharField(max_length=16, unique=True, verbose_name='任务编号')),
                ('filepub_time', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('file_content', models.FileField(upload_to='./upload/', verbose_name='存储文件')),
                ('task_remark', models.CharField(max_length=255, verbose_name='文档备注')),
            ],
        ),
        migrations.CreateModel(
            name='eva_recollect',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('eva_id', models.CharField(max_length=16, verbose_name='评价问卷编号')),
                ('eva_time', models.DateTimeField(auto_now_add=True, verbose_name='评价时间')),
                ('act_name', models.CharField(max_length=64, verbose_name='活动名称')),
                ('valuer_name', models.CharField(max_length=32, verbose_name='评价者')),
                ('beeva_name', models.CharField(max_length=32, verbose_name='被评价者')),
                ('eva_score', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='得分')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('evaluate_id', models.IntegerField(unique=True, verbose_name='评价编号')),
                ('evaluate_type', models.CharField(max_length=16, verbose_name='评价类型')),
                ('evaluate_item', models.CharField(max_length=55, verbose_name='评价项目')),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('evaluate_weight', models.IntegerField(default=0, verbose_name='评价权重')),
            ],
        ),
        migrations.CreateModel(
            name='feed_back',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group_id', models.IntegerField(unique=True, verbose_name='小组编号')),
                ('feedback_time', models.DateTimeField(auto_now_add=True, verbose_name='反馈时间')),
                ('feedback_type', models.CharField(max_length=32, verbose_name='反馈类型')),
                ('feedback_content', models.CharField(max_length=255, verbose_name='反馈内容')),
            ],
        ),
        migrations.CreateModel(
            name='group_grade',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group_id', models.IntegerField(unique=True, verbose_name='小组编号')),
                ('learn_topic', models.CharField(max_length=255, verbose_name='学习主题')),
                ('group_score', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='小组得分')),
                ('num', models.CharField(max_length=11, unique=True, verbose_name='学生学号')),
                ('single_score', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='个人得分')),
            ],
        ),
        migrations.CreateModel(
            name='group_record',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group_id', models.IntegerField(unique=True, verbose_name='小组编号')),
                ('record_time', models.DateTimeField(auto_now_add=True, verbose_name='会议时间')),
                ('record_topic', models.CharField(max_length=255, verbose_name='会议主题')),
                ('record_content', models.CharField(max_length=255, verbose_name='会议内容')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num', models.CharField(max_length=11, unique=True, verbose_name='学生学号')),
                ('name', models.CharField(max_length=32, verbose_name='学生姓名')),
                ('grade', models.CharField(max_length=16, verbose_name='学生班级')),
                ('score', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('group_id', models.IntegerField(unique=True, verbose_name='小组编号')),
                ('group_role', models.CharField(max_length=32, verbose_name='组内角色')),
            ],
        ),
        migrations.CreateModel(
            name='task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='总编号')),
                ('group_id', models.IntegerField(unique=True, verbose_name='小组编号')),
                ('num', models.CharField(max_length=11, unique=True, verbose_name='学生学号')),
                ('group_role', models.CharField(max_length=32, verbose_name='组内角色')),
                ('task_id', models.CharField(max_length=16, unique=True, verbose_name='任务编号')),
                ('task_content', models.CharField(max_length=255, unique=True, verbose_name='任务内容')),
                ('start_time', models.DateField(verbose_name='上传时间')),
                ('end_time', models.DateField(verbose_name='上传时间')),
                ('is_finish', models.BooleanField(default=False, verbose_name='是否完成')),
                ('is_overtime', models.BooleanField(default=False, verbose_name='是否超时')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group_id', models.IntegerField(unique=True, verbose_name='小组编号')),
                ('topic', models.CharField(max_length=255, verbose_name='学习主题')),
                ('group_score', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
