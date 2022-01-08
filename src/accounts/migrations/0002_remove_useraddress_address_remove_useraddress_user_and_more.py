# Generated by Django 4.0 on 2022-01-06 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='address',
        ),
        migrations.RemoveField(
            model_name='useraddress',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='addresses',
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='accounts.customer'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('ادمین سایت', 'ادمین سایت'), ('مدیر رستوران', 'مدیر رستوران'), ('مشتری', 'مشتری')], default='ادمین سایت', max_length=20),
        ),
    ]