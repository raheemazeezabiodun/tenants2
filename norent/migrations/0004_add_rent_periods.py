# Generated by Django 2.2.13 on 2020-10-05 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('norent', '0003_localize'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='rent_periods',
            field=models.ManyToManyField(to='norent.RentPeriod'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='rent_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foreignkey_rent_periods', to='norent.RentPeriod'),
        ),
    ]