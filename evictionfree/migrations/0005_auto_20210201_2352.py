# Generated by Django 2.2.18 on 2021-02-01 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evictionfree', '0004_submittedhardshipdeclaration_fully_processed_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evictionfreeuser',
            options={'permissions': [('view_evictionfree_rtc_users', 'Can view/download EvictionFreeNY.org user data on behalf of RTC'), ('view_evictionfree_hj4a_users', 'Can view/download EvictionFreeNY.org user data on behalf of HJ4A')], 'verbose_name': 'User with EvictionFreeNY declaration', 'verbose_name_plural': 'Users with EvictionFreeNY declarations'},
        ),
    ]