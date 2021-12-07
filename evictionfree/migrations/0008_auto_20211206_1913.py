# Generated by Django 3.2.5 on 2021-12-06 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evictionfree', '0007_auto_20210412_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submittedhardshipdeclaration',
            name='lob_letter_object',
            field=models.JSONField(blank=True, help_text='If the mail item was sent via Lob, this is the JSON response of the API call that was made to send the mail item, documented at https://lob.com/docs/python#letters.', null=True),
        ),
        migrations.AlterField(
            model_name='submittedhardshipdeclaration',
            name='locale',
            field=models.CharField(choices=[('en', 'English'), ('es', 'Spanish')], default='en', help_text="The locale of the user who sent the mail item, at the time that they sent it. Note that this may be different from the user's current locale, e.g. if they changed it after sending the mail item.", max_length=5),
        ),
        migrations.AlterField(
            model_name='submittedhardshipdeclaration',
            name='tracking_number',
            field=models.CharField(blank=True, help_text='The USPS tracking number for the mail item.', max_length=100),
        ),
    ]
