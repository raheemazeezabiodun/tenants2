# Generated by Django 3.2 on 2021-04-12 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0026_auto_20210211_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivedletterrequest',
            name='lob_letter_object',
            field=models.JSONField(blank=True, help_text='If the letter was sent via Lob, this is the JSON response of the API call that was made to send the letter, documented at https://lob.com/docs/python#letters.', null=True),
        ),
        migrations.AlterField(
            model_name='letterrequest',
            name='lob_letter_object',
            field=models.JSONField(blank=True, help_text='If the letter was sent via Lob, this is the JSON response of the API call that was made to send the letter, documented at https://lob.com/docs/python#letters.', null=True),
        ),
    ]
