# Generated by Django 2.2.10 on 2020-02-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapidpro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('uuid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=10)),
            ],
        ),
    ]