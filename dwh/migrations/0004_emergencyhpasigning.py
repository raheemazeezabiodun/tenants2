# Generated by Django 2.2.10 on 2020-06-01 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwh', '0003_letterofcomplaintrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmergencyHPASigning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
            ],
        ),
    ]