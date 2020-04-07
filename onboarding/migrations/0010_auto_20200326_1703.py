# Generated by Django 2.2.10 on 2020-03-26 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0009_onboardinginfo_floor_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardinginfo',
            name='signup_intent',
            field=models.CharField(choices=[('LOC', 'Letter of Complaint'), ('HP', 'HP Action'), ('EHP', 'Emergency HP Action')], help_text='The reason the user originally signed up with us.', max_length=30),
        ),
    ]
