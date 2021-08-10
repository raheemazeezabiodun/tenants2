# Generated by Django 3.2 on 2021-07-12 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("onboarding", "0025_auto_20210707_1943"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onboardinginfo",
            name="lease_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("RENT_STABILIZED", "Rent Stabilized/Rent Controlled"),
                    ("OTHER_AFFORDABLE", "Affordable housing (other than rent-stabilized)"),
                    ("MARKET_RATE", "Market Rate"),
                    ("NYCHA", "NYCHA/Public Housing"),
                    ("NOT_SURE", "I'm not sure"),
                    ("NO_LEASE", "I don't have a lease"),
                ],
                help_text="The type of housing the user lives in (NYC only).",
                max_length=30,
            ),
        ),
    ]