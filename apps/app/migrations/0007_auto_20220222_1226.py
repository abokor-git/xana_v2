# Generated by Django 3.2.6 on 2022-02-22 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_packagedata_balance_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='ip_adresse_client',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='queuehist',
            name='ip_adresse_client',
            field=models.CharField(max_length=255, null=True),
        ),
    ]