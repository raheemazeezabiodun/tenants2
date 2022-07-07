# Generated by Django 3.2.13 on 2022-06-29 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laletterbuilder', '0005_auto_20220615_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitabilityletter',
            name='pdf_base64',
            field=models.TextField(blank=True, help_text='A base64 encoded string representing the English content of the letter.'),
        ),
    ]
