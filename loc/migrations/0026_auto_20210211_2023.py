# Generated by Django 2.2.18 on 2021-02-11 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0025_archivedletterrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivedletterrequest',
            name='rejection_reason',
            field=models.CharField(blank=True, choices=[('INCRIMINATION', 'Letter is potentially incriminating'), ('NOT_REPAIR_RELATED', 'Issues are not repair-related'), ('CHANGED_MIND', 'Tenant changed their mind'), ('BAD_ADDRESS', 'Unintelligible address'), ('OTHER', 'Other')], help_text="The reason we didn't mail the letter, if applicable.", max_length=100),
        ),
        migrations.AlterField(
            model_name='letterrequest',
            name='rejection_reason',
            field=models.CharField(blank=True, choices=[('INCRIMINATION', 'Letter is potentially incriminating'), ('NOT_REPAIR_RELATED', 'Issues are not repair-related'), ('CHANGED_MIND', 'Tenant changed their mind'), ('BAD_ADDRESS', 'Unintelligible address'), ('OTHER', 'Other')], help_text="The reason we didn't mail the letter, if applicable.", max_length=100),
        ),
    ]
