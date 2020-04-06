# Generated by Django 2.2.10 on 2020-04-06 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpaction', '0019_docusignenvelope'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manhattan_court_email', models.EmailField(blank=True, max_length=254)),
                ('bronx_court_email', models.EmailField(blank=True, max_length=254)),
                ('brooklyn_court_email', models.EmailField(blank=True, max_length=254)),
                ('queens_court_email', models.EmailField(blank=True, max_length=254)),
                ('staten_island_court_email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
    ]
