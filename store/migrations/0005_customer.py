# Generated by Django 3.1.5 on 2021-01-25 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=500)),
            ],
        ),
    ]
