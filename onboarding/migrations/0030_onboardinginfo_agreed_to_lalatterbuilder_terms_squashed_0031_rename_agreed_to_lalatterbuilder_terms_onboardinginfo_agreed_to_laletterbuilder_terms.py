# Generated by Django 3.2.5 on 2021-11-30 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('onboarding', '0030_onboardinginfo_agreed_to_lalatterbuilder_terms'), ('onboarding', '0031_rename_agreed_to_lalatterbuilder_terms_onboardinginfo_agreed_to_laletterbuilder_terms')]

    dependencies = [
        ('onboarding', '0029_alter_onboardinginfo_signup_intent'),
    ]

    operations = [
        migrations.AddField(
            model_name='onboardinginfo',
            name='agreed_to_laletterbuilder_terms',
            field=models.BooleanField(default=False, help_text='Whether the user has agreed to the LA Letter Builder terms of service and privacy policy.'),
        ),
    ]
