# Generated by Django 4.0 on 2021-12-26 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Site Admin', 'Site Admin'), ('Restaurant Manager', 'Restaurant Manager'), ('Customer', 'Customer')], max_length=20),
        ),
    ]
