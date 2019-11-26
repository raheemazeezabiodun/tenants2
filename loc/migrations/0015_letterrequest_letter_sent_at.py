# Generated by Django 2.2.4 on 2019-11-13 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0014_letterrequest_tracking_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='letterrequest',
            name='letter_sent_at',
            field=models.DateTimeField(blank=True, help_text='When the letter was mailed through the postal service.', null=True),
        ),
    ]