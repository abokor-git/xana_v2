# Generated by Django 3.2.6 on 2022-02-22 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_packagedata_quantite_voix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagedata',
            name='balance_data',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
