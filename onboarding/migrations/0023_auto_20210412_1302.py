# Generated by Django 3.2 on 2021-04-12 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0022_onboardinginfo_geocoded_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onboardinginfo',
            name='can_receive_rttc_comms',
            field=models.BooleanField(blank=True, help_text='Whether the user has opted-in to being contacted by the Right to the City Alliance (RTTC).', null=True),
        ),
        migrations.AlterField(
            model_name='onboardinginfo',
            name='can_receive_saje_comms',
            field=models.BooleanField(blank=True, help_text='Whether the user has opted-in to being contacted by Strategic Actions for a Just Economy (SAJE).', null=True),
        ),
        migrations.AlterField(
            model_name='onboardinginfo',
            name='geometry',
            field=models.JSONField(blank=True, help_text="The GeoJSON point representing the user's address, if available.", null=True),
        ),
        migrations.AlterField(
            model_name='onboardinginfo',
            name='has_called_311',
            field=models.BooleanField(blank=True, help_text='Has the user called 311 before?', null=True),
        ),
        migrations.AlterField(
            model_name='onboardinginfo',
            name='has_no_services',
            field=models.BooleanField(blank=True, help_text='Is the user missing essential services like water?', null=True),
        ),
        migrations.AlterField(
            model_name='onboardinginfo',
            name='has_pests',
            field=models.BooleanField(blank=True, help_text='Does the user have pests like rodents or bed bugs?', null=True),
        ),
        migrations.AlterField(
            model_name='onboardinginfo',
            name='is_in_eviction',
            field=models.BooleanField(blank=True, help_text='Has the user received an eviction notice?', null=True),
        ),
        migrations.AlterField(
            model_name='onboardinginfo',
            name='needs_repairs',
            field=models.BooleanField(blank=True, help_text='Does the user need repairs in their apartment?', null=True),
        ),
        migrations.AlterField(
            model_name='onboardinginfo',
            name='receives_public_assistance',
            field=models.BooleanField(blank=True, help_text='Does the user receive public assistance, e.g. Section 8?', null=True),
        ),
    ]