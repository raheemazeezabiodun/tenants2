# Generated by Django 3.2 on 2021-05-06 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('norent', '0010_alter_letter_lob_letter_object'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityWithoutStateDiagnostic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]