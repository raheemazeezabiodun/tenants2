# Generated by Django 2.2.13 on 2021-01-29 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evictionfree', '0003_submittedhardshipdeclaration_emailed_to_user_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='submittedhardshipdeclaration',
            name='fully_processed_at',
            field=models.DateTimeField(blank=True, help_text='When the declaration was fully processed, i.e. sent to all relevant parties.', null=True),
        ),
    ]