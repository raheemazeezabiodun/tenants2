# Generated by Django 2.2.18 on 2021-02-05 10:59

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loc', '0024_auto_20200826_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedLetterRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('mail_choice', models.TextField(choices=[('WE_WILL_MAIL', 'Yes, have JustFix.nyc mail this letter for me.'), ('USER_WILL_MAIL', "No thanks, I'll mail it myself.")], help_text='How the letter of complaint will be mailed.', max_length=30)),
                ('html_content', models.TextField(blank=True, help_text='The HTML content of the letter at the time it was requested.')),
                ('lob_letter_object', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='If the letter was sent via Lob, this is the JSON response of the API call that was made to send the letter, documented at https://lob.com/docs/python#letters.', null=True)),
                ('tracking_number', models.CharField(blank=True, help_text='The tracking number for the letter. Note that when this is changed, the user will be notified via SMS and added to a LOC follow-up campaign, if one has been configured.', max_length=100)),
                ('letter_sent_at', models.DateTimeField(blank=True, help_text='When the letter was mailed through the postal service.', null=True)),
                ('rejection_reason', models.CharField(blank=True, choices=[('INCRIMINATION', 'Letter is potentially incriminating'), ('CHANGED_MIND', 'Tenant changed their mind'), ('BAD_ADDRESS', 'Unintelligible address'), ('OTHER', 'Other')], help_text="The reason we didn't mail the letter, if applicable.", max_length=100)),
                ('archived_at', models.DateTimeField(help_text='When the LetterRequest this is based on was archived.')),
                ('original_letter_request_id', models.IntegerField(help_text='The original primary key of the deleted LetterRequest this is based on.')),
                ('notes', models.TextField(blank=True, help_text='Any additional notes about the archiving of this letter request, e.g. the reason for its archiving.')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archived_letter_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
