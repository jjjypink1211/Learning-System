# Generated by Django 3.2.8 on 2022-04-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0025_auto_20220402_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='is_check',
            field=models.BooleanField(verbose_name='是否通过审核'),
        ),
        migrations.AlterField(
            model_name='doc',
            name='submit_type',
            field=models.CharField(max_length=3, verbose_name='任务类型'),
        ),
    ]