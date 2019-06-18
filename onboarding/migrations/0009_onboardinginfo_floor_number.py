# Generated by Django 2.1.8 on 2019-06-18 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0008_onboardinginfo_pad_bin'),
    ]

    operations = [
        migrations.AddField(
            model_name='onboardinginfo',
            name='floor_number',
            field=models.PositiveSmallIntegerField(blank=True, help_text="The floor number the user's apartment is on.", null=True),
        ),
    ]
