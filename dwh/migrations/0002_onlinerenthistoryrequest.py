# Generated by Django 2.2.10 on 2020-02-19 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineRentHistoryRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('user_uuid', models.CharField(blank=True, max_length=36, null=True)),
            ],
        ),
    ]