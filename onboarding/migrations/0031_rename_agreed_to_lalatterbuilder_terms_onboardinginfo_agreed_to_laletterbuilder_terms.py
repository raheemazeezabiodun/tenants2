# Generated by Django 3.2.5 on 2021-11-29 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0030_onboardinginfo_agreed_to_lalatterbuilder_terms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='onboardinginfo',
            old_name='agreed_to_lalatterbuilder_terms',
            new_name='agreed_to_laletterbuilder_terms',
        ),
    ]
