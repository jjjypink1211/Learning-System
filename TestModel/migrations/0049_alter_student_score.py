# Generated by Django 3.2.8 on 2022-04-25 10:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0048_alter_usergroup_group_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='score',
            field=models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]