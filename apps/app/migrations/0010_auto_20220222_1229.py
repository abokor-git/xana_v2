# Generated by Django 3.2.6 on 2022-02-22 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20220222_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='error_description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='queuehist',
            name='error_description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
