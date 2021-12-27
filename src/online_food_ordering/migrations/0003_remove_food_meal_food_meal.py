# Generated by Django 4.0 on 2021-12-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_food_ordering', '0002_alter_branch_options_alter_category_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='meal',
        ),
        migrations.AddField(
            model_name='food',
            name='meal',
            field=models.ManyToManyField(to='online_food_ordering.Meal'),
        ),
    ]
