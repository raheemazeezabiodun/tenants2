# Generated by Django 3.2 on 2021-04-09 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_add_impersonate_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='justfixuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
