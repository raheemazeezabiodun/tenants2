# Generated by Django 2.2.10 on 2020-03-30 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0011_auto_20200329_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='value',
            field=models.CharField(choices=[('HOME__COVID_SANITATION_REQUIRED', 'Needs cleaning due to COVID-19'), ('HOME__MICE', 'Mice'), ('HOME__RATS', 'Rats'), ('HOME__COCKROACHES', 'Cockroaches'), ('HOME__NO_GAS', 'No Gas'), ('HOME__NO_HEAT', 'No Heat'), ('HOME__NO_HOT_WATER', 'No Hot Water'), ('HOME__NO_COLD_WATER', 'No Cold Water'), ('HOME__NO_SMOKE_DETECTOR', 'No Smoke Detector'), ('HOME__SMOKE_DETECTOR_DEFECTIVE', 'Smoke Detector Defective'), ('HOME__FLOOR', 'Floor Sags'), ('HOME__PAINTING', 'Apartment Needs Painting'), ('HOME__FRONT_DOOR_DEFECTIVE', 'Front Door Defective'), ('HOME__FRONT_DOOR_BROKEN', 'Front Door Broken'), ('HOME__DOOR_LOCK_DEFECTIVE', 'Door Lock Defective'), ('HOME__DOOR_LOCK_BROKEN', 'Door Lock Broken'), ('HOME__DOORBELL_DEFECTIVE', 'Doorbell Defective'), ('HOME__DOORBELL_BROKEN', 'Doorbell Broken'), ('HOME__BUZZER_DEFECTIVE', 'Buzzer Defective'), ('HOME__BUZZER_BROKEN', 'Buzzer Broken'), ('HOME__LEAD_BASED_PAINT', 'Lead-based Paint'), ('HOME__VACATE_ORDER_ISSUED', 'Vacate Order Issued'), ('BEDROOMS__PAINT', 'Peeling paint'), ('BEDROOMS__WALLS', 'Cracked walls'), ('BEDROOMS__MOLD_ON_WALLS', 'Mold on Walls'), ('BEDROOMS__WATER_DAMAGE', 'Water Damage'), ('BEDROOMS__LOOSE_FLOOR', 'Loose Floor'), ('BEDROOMS__BASEBOARDS_DEFECTIVE', 'Baseboards Defective'), ('BEDROOMS__WINDOW_GLASS_BROKEN', 'Window Glass Broken'), ('BEDROOMS__WINDOW_FRAME_DEFECTIVE', 'Window Frame Defective'), ('BEDROOMS__DOOR', 'Door Broken'), ('BEDROOMS__RADIATORS', 'Radiators/Risers Defective'), ('BEDROOMS__CEILING', 'Ceiling Falling/Fell'), ('BEDROOMS__CEILING_LEAKING', 'Ceiling Leaking'), ('BEDROOMS__ELECTRICITY', 'Electricity defective'), ('BEDROOMS__WIRING_EXPOSED', 'Electric wiring exposed'), ('BEDROOMS__OUTLETS', 'Outlets defective'), ('KITCHEN__MOLD', 'Mold on walls'), ('KITCHEN__WATER', 'Water damage'), ('KITCHEN__PAINT', 'Peeling Paint'), ('KITCHEN__WALLS', 'Cracked walls'), ('KITCHEN__LOOSE_FLOOR', 'Loose Floor'), ('KITCHEN__BASEBOARDS_DEFECTIVE', 'Baseboards Defective'), ('KITCHEN__WINDOW_GLASS_BROKEN', 'Window Glass Broken'), ('KITCHEN__WINDOW_FRAME_DEFECTIVE', 'Window Frame Defective'), ('KITCHEN__DOOR', 'Door Broken'), ('KITCHEN__RADIATORS', 'Radiators/Risers Defective'), ('KITCHEN__CEILING', 'Ceiling Falling/Fell'), ('KITCHEN__CEILING_LEAKING', 'Ceiling Leaking'), ('KITCHEN__ELECTRICITY', 'Electricity defective'), ('KITCHEN__WIRING_EXPOSED', 'Electric wiring exposed'), ('KITCHEN__OUTLETS', 'Outlets defective'), ('KITCHEN__REFRIGERATOR', 'Refrigerator Defective'), ('KITCHEN__REFRIGERATOR_BROKEN', 'Refrigerator Broken'), ('KITCHEN__STOVE', 'Stove Defective'), ('KITCHEN__STOVE_BROKEN', 'Stove Broken'), ('KITCHEN__SINK', 'Cracked Sink'), ('KITCHEN__FAUCET_LEAKING', 'Leaky Faucet'), ('KITCHEN__NO_FAUCET', 'Faucets not installed'), ('KITCHEN__FAUCET_NOT_WORKING', 'Faucets not working'), ('KITCHEN__WATER_PRESSURE', 'Inadequate Water pressure'), ('KITCHEN__PIPES', 'Pipes Leaking'), ('KITCHEN__DRAIN', 'Drain Stoppage'), ('LIVING_ROOM__MOLD', 'Mold on walls'), ('LIVING_ROOM__WATER', 'Water damage'), ('LIVING_ROOM__PAINT', 'Peeling paint'), ('LIVING_ROOM__WALLS', 'Cracked walls'), ('LIVING_ROOM__LOOSE_FLOOR', 'Loose Floor'), ('LIVING_ROOM__BASEBOARDS_DEFECTIVE', 'Baseboards Defective'), ('LIVING_ROOM__WINDOW_GLASS_BROKEN', 'Window Glass Broken'), ('LIVING_ROOM__WINDOW_FRAME_DEFECTIVE', 'Window Frame Defective'), ('LIVING_ROOM__DOOR', 'Door Broken'), ('LIVING_ROOM__RADIATORS', 'Radiators/Risers Defective'), ('LIVING_ROOM__CEILING', 'Ceiling Falling/Fell'), ('LIVING_ROOM__CEILING_LEAKING', 'Ceiling Leaking'), ('LIVING_ROOM__ELECTRICITY', 'Electricity defective'), ('LIVING_ROOM__WIRING_EXPOSED', 'Electric wiring exposed'), ('LIVING_ROOM__OUTLETS', 'Outlets defective'), ('BATHROOMS__MOLD', 'Mold on walls'), ('BATHROOMS__WATER', 'Water damage'), ('BATHROOMS__PAINT', 'Peeling paint'), ('BATHROOMS__WALLS', 'Cracked walls'), ('BATHROOMS__LOOSE_FLOOR', 'Loose Floor'), ('BATHROOMS__BASEBOARDS_DEFECTIVE', 'Baseboards Defective'), ('BATHROOMS__WINDOW_GLASS_BROKEN', 'Window Glass Broken'), ('BATHROOMS__WINDOW_FRAME_DEFECTIVE', 'Window Frame Defective'), ('BATHROOMS__DOOR', 'Door Broken'), ('BATHROOMS__RADIATORS', 'Radiators/Risers Defective'), ('BATHROOMS__CEILING', 'Ceiling Falling/Fell'), ('BATHROOMS__CEILING_LEAKING', 'Ceiling Leaking'), ('BATHROOMS__ELECTRICITY', 'Electricity defective'), ('BATHROOMS__WIRING_EXPOSED', 'Electric wiring exposed'), ('BATHROOMS__OUTLETS', 'Outlets defective'), ('BATHROOMS__TOILET', 'Toilet not working'), ('BATHROOMS__TOILET_LEAKING', 'Toilet leaking'), ('BATHROOMS__SINK', 'Sink: Cracked Sink'), ('BATHROOMS__SINK_FAUCET_LEAKING', 'Sink: Leaky Faucet'), ('BATHROOMS__SINK_NO_FAUCET', 'Sink: Faucets not installed'), ('BATHROOMS__SINK_FAUCET_NOT_WORKING', 'Sink: Faucets not working'), ('BATHROOMS__SINK_WATER_PRESSURE', 'Sink: Low Water pressure'), ('BATHROOMS__SINK_PIPES', 'Sink: Pipes Leaking'), ('BATHROOMS__SINK_DRAIN', 'Sink: Drain Stoppage'), ('BATHROOMS__TUB', 'Bathtub: Cracked Tub'), ('BATHROOMS__TUB_FAUCET_LEAKING', 'Bathtub: Leaky Faucet'), ('BATHROOMS__TUB_NO_FAUCET', 'Bathtub: Faucets not installed'), ('BATHROOMS__TUB_FAUCET_NOT_WORKING', 'Bathtub: Faucets not working'), ('BATHROOMS__TUB_PIPES', 'Bathtub: Pipes Leaking'), ('BATHROOMS__TUB_DRAIN', 'Bathtub: Drain Stoppage'), ('BATHROOMS__SHOWER_MOLD', 'Shower: Mold on walls'), ('BATHROOMS__SHOWER_WATER_PRESSURE', 'Shower: Wall tiles cracked'), ('BATHROOMS__SHOWER_PIPES', 'Shower: Wall tiles missing'), ('BATHROOMS__SHOWER', 'Shower: Not Working'), ('BATHROOMS__SHOWER_FAUCET_LEAKING', 'Shower: Low Water pressure'), ('BATHROOMS__SHOWER_NO_FAUCET', 'Shower: Leaky shower head'), ('BATHROOMS__SHOWER_DRAIN', 'Shower: Drain Stoppage'), ('PUBLIC_AREAS__COVID_SANITATION_REQUIRED', 'Needs cleaning due to COVID-19'), ('PUBLIC_AREAS__PAINTING_OVERDUE', 'Painting overdue (3 years)'), ('PUBLIC_AREAS__PAINT', 'Peeling/flaking paint'), ('PUBLIC_AREAS__NO_HEAT', 'No Heat'), ('PUBLIC_AREAS__NO_HOT_WATER', 'No Hot Water'), ('PUBLIC_AREAS__WATER_PRESSURE', 'Inadequate water pressure'), ('PUBLIC_AREAS__RUSTY_WATER', 'Rusty water'), ('PUBLIC_AREAS__WIRING_EXPOSED', 'Electric wiring exposed'), ('PUBLIC_AREAS__ELECTRICAL_CURRENT', 'Weak electrical current'), ('PUBLIC_AREAS__BUGS', 'Bug Infestation'), ('PUBLIC_AREAS__PESTS', 'Rats/Mice'), ('PUBLIC_AREAS__FUMES', 'Fumes/smoke entering apartment'), ('PUBLIC_AREAS__SMOKE_DETECTORS', 'Broken/no smoke/Co2 detector'), ('PUBLIC_AREAS__WINDOW_GUARDS', 'Window guards missing'), ('PUBLIC_AREAS__ILLEGAL_APARTMENTS', 'Illegal apartments in basement'), ('PUBLIC_AREAS__NO_SUPER', 'Inadequate / no super service'), ('PUBLIC_AREAS__RENT_RECEIPTS', 'No rent receipts given'), ('PUBLIC_AREAS__INCOMPLETE_RENT_RECEIPTS', 'Rent receipts incomplete'), ('LANDLORD__RETALIATION', 'Retaliation for seeking repair'), ('LANDLORD__RENT', 'Not receiving rent receipts'), ('LANDLORD__NO_LEASE', 'No lease'), ('LANDLORD__DOCUMENTS', 'False documents'), ('LANDLORD__CONSTRUCTION', 'Illegal construction'), ('LANDLORD__MCI', 'Repeated MCI'), ('LANDLORD__OVERCHARGE', 'Overcharging'), ('LANDLORD__HOLDOVER', 'Holdover cases'), ('LANDLORD__FORCE', 'Using force / threats of force'), ('LANDLORD__STOPPING_SERVICES', 'Stopping essential services'), ('LANDLORD__REMOVING_POSSESSIONS', 'Removing possessions from unit'), ('LANDLORD__CHANGING_LOCKS', 'Changing locks without new key'), ('LANDLORD__BUYOUT', 'Constant buyout demands'), ('LANDLORD__TREATENING_EVICTION', 'False claim eviction threat')], help_text='The issue the user has reported.', max_length=60),
        ),
    ]
