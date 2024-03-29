# Generated by Django 4.0 on 2021-12-31 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('primary', models.BooleanField()),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.address')),
            ],
            options={
                'verbose_name_plural': 'branches',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(upload_to='food_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_food_ordering.category')),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='online_food_ordering.branch')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='online_food_ordering.food')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('سفارش', 'سفارش'), ('ثبت', 'ثبت'), ('ارسال', 'ارسال'), ('تحویل', 'تحویل')], max_length=10)),
                ('user_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.useraddress')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='online_food_ordering.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='online_food_ordering.order')),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='meals',
            field=models.ManyToManyField(to='online_food_ordering.Meal'),
        ),
        migrations.AddField(
            model_name='branch',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='online_food_ordering.category'),
        ),
        migrations.AddField(
            model_name='branch',
            name='manager',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.restaurantmanager'),
        ),
        migrations.AddField(
            model_name='branch',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='online_food_ordering.restaurant'),
        ),
    ]
