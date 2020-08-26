# Generated by Django 2.2.13 on 2020-08-26 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpaction', '0023_courtcontact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servingpapers',
            name='primary_line',
            field=models.CharField(blank=True, help_text='Usually the first line of the address, e.g. "150 Court Street"', max_length=64),
        ),
        migrations.AlterField(
            model_name='servingpapers',
            name='secondary_line',
            field=models.CharField(blank=True, help_text='Optional. Usually the second line of the address, e.g. "Suite 2"', max_length=64),
        ),
    ]