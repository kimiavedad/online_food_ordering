# Generated by Django 4.0 on 2022-01-03 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('ادمین سایت', 'ادمین سایت'), ('مدیر رستوران', 'مدیر رستوران'), ('مشتری', 'مشتری')], default='ادمین سایت', max_length=20),
        ),
    ]
