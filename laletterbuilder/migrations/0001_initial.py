# Generated by Django 3.2.12 on 2022-03-08 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import project.util.lob_django_util


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HabitabilityLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('locale', models.CharField(choices=[('en', 'English'), ('es', 'Spanish')], default='en', help_text="The locale of the user who sent the mail item, at the time that they sent it. Note that this may be different from the user's current locale, e.g. if they changed it after sending the mail item.", max_length=5)),
                ('lob_letter_object', models.JSONField(blank=True, help_text='If the mail item was sent via Lob, this is the JSON response of the API call that was made to send the mail item, documented at https://lob.com/docs/python#letters.', null=True)),
                ('tracking_number', models.CharField(blank=True, help_text='The USPS tracking number for the mail item.', max_length=100)),
                ('html_content', models.TextField(help_text='The HTML content of the letter at the time it was sent, in English.')),
                ('localized_html_content', models.TextField(blank=True, help_text="The HTML content of the letter at the time it was sent, in the user's locale at the time they sent it. If the user's locale is English, this will be blank (since the English version is already stored in another field).")),
                ('letter_sent_at', models.DateTimeField(blank=True, help_text='When the letter was mailed.', null=True)),
                ('letter_emailed_at', models.DateTimeField(blank=True, help_text='When the letter was e-mailed.', null=True)),
                ('fully_processed_at', models.DateTimeField(blank=True, help_text='When the letter was fully processed, i.e. sent to all relevant parties.', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laletterbuilder_letters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
            bases=(models.Model, project.util.lob_django_util.SendableViaLobMixin),
        ),
    ]
