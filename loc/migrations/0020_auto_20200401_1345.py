# Generated by Django 2.2.10 on 2020-04-01 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loc', '0019_auto_20200401_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='landlorddetails',
            name='city',
            field=models.CharField(blank=True, help_text='The city of the address, e.g. "Brooklyn".', max_length=80),
        ),
        migrations.AddField(
            model_name='landlorddetails',
            name='primary_line',
            field=models.CharField(blank=True, help_text='Usually the first line of the address, e.g. "150 Court Street"', max_length=255),
        ),
        migrations.AddField(
            model_name='landlorddetails',
            name='secondary_line',
            field=models.CharField(blank=True, help_text='Optional. Usually the second line of the address, e.g. "Suite 2"', max_length=255),
        ),
        migrations.AddField(
            model_name='landlorddetails',
            name='state',
            field=models.CharField(blank=True, choices=[('AK', 'Alaska'), ('AL', 'Alabama'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MP', 'Northern Mariana Islands'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('VI', 'Virgin Islands'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], help_text='The two-letter state or territory for the address, e.g. "NY".', max_length=2),
        ),
        migrations.AddField(
            model_name='landlorddetails',
            name='urbanization',
            field=models.CharField(blank=True, help_text='Optional. Only used for addresses in Puerto Rico.', max_length=80),
        ),
        migrations.AddField(
            model_name='landlorddetails',
            name='zip_code',
            field=models.CharField(blank=True, help_text='The zip code of the address, e.g. "11201" or "94107-2282".', max_length=10),
        ),
        migrations.AlterField(
            model_name='landlorddetails',
            name='address',
            field=models.CharField(verbose_name="LEGACY address", help_text='The full mailing address for the landlord. This is a LEGACY field that we prefer not to use if possible, e.g. if the more granular primary/secondary line and city/state/zip details are available on this model.', max_length=1000),
        ),
    ]
