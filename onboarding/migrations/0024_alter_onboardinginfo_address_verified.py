# Generated by Django 3.2 on 2021-04-19 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0023_auto_20210412_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardinginfo',
            name='address_verified',
            field=models.BooleanField(default=False, help_text="Whether we've verified, on the server-side, that the user's address is valid."),
        ),
    ]
