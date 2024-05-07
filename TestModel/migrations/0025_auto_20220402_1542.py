# Generated by Django 3.2.8 on 2022-04-02 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0024_alter_task_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='is_check',
            field=models.BooleanField(default=False, verbose_name='是否通过审核'),
        ),
        migrations.AddField(
            model_name='doc',
            name='submit_time',
            field=models.DateField(default=1, verbose_name='上传时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='doc',
            name='submit_type',
            field=models.BooleanField(default=False, verbose_name='上传类型'),
        ),
        migrations.AlterField(
            model_name='doc',
            name='file_content',
            field=models.CharField(max_length=255, verbose_name='文件路径/文本'),
        ),
    ]