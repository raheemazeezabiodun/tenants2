# Generated by Django 2.2.10 on 2020-04-04 11:39

from django.db import migrations, models
import project.util.mailing_address


class Migration(migrations.Migration):

    dependencies = [
        ('nycha', '0002_auto_20200401_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nychaoffice',
            name='zip_code',
            field=models.CharField(blank=True, help_text='The zip code of the address, e.g. "11201" or "94107-2282".', max_length=10, validators=[project.util.mailing_address.ZipCodeValidator()]),
        ),
    ]