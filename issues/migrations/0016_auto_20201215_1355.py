# Generated by Django 2.2.13 on 2020-12-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0015_auto_20201120_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='value',
            field=models.CharField(choices=[('HOME__COVID_SANITATION_REQUIRED', 'Needs cleaning due to COVID-19'), ('HOME__MICE', 'Mice'), ('HOME__RATS', 'Rats'), ('HOME__COCKROACHES', 'Cockroaches'), ('HOME__NO_GAS', 'No gas'), ('HOME__NO_HEAT', 'No heat'), ('HOME__NO_HOT_WATER', 'No hot water'), ('HOME__NO_COLD_WATER', 'No cold water'), ('HOME__NO_SMOKE_DETECTOR', 'No smoke detector'), ('HOME__SMOKE_DETECTOR_DEFECTIVE', 'Smoke detector not working'), ('HOME__FLOOR', 'Floor sags'), ('HOME__PAINTING', 'Apartment needs painting'), ('HOME__FRONT_DOOR_DEFECTIVE', 'Front door not working'), ('HOME__FRONT_DOOR_BROKEN', 'Front door broken'), ('HOME__DOOR_LOCK_DEFECTIVE', 'Door lock not working'), ('HOME__DOOR_LOCK_BROKEN', 'Door lock broken'), ('HOME__DOORBELL_DEFECTIVE', 'Doorbell not working'), ('HOME__DOORBELL_BROKEN', 'Doorbell broken'), ('HOME__BUZZER_DEFECTIVE', 'Buzzer not working'), ('HOME__BUZZER_BROKEN', 'Buzzer broken'), ('HOME__LEAD_BASED_PAINT', 'Lead-based paint'), ('HOME__VACATE_ORDER_ISSUED', 'Vacate order issued'), ('HOME__MOLD', 'Mold'), ('BEDROOMS__PAINT', 'Peeling paint'), ('BEDROOMS__WALLS', 'Cracked walls'), ('BEDROOMS__MOLD_ON_WALLS', 'Mold on walls'), ('BEDROOMS__WATER_DAMAGE', 'Water damage'), ('BEDROOMS__LOOSE_FLOOR', 'Loose floor'), ('BEDROOMS__BASEBOARDS_DEFECTIVE', 'Baseboards defective'), ('BEDROOMS__WINDOW_GLASS_BROKEN', 'Window glass broken'), ('BEDROOMS__WINDOW_FRAME_DEFECTIVE', 'Window frame defective'), ('BEDROOMS__DOOR', 'Door not working'), ('BEDROOMS__RADIATORS', 'Radiators/risers not working'), ('BEDROOMS__CEILING', 'Ceiling falling/fell'), ('BEDROOMS__CEILING_LEAKING', 'Ceiling leaking'), ('BEDROOMS__ELECTRICITY', 'Electricity not working'), ('BEDROOMS__WIRING_EXPOSED', 'Electric wiring exposed'), ('BEDROOMS__OUTLETS', 'Outlets not working'), ('KITCHEN__MOLD', 'Mold on walls'), ('KITCHEN__WATER', 'Water damage'), ('KITCHEN__PAINT', 'Peeling paint'), ('KITCHEN__WALLS', 'Cracked walls'), ('KITCHEN__LOOSE_FLOOR', 'Loose floor'), ('KITCHEN__BASEBOARDS_DEFECTIVE', 'Baseboards defective'), ('KITCHEN__WINDOW_GLASS_BROKEN', 'Window glass broken'), ('KITCHEN__WINDOW_FRAME_DEFECTIVE', 'Window frame defective'), ('KITCHEN__DOOR', 'Door not working'), ('KITCHEN__RADIATORS', 'Radiators/risers not working'), ('KITCHEN__CEILING', 'Ceiling falling/fell'), ('KITCHEN__CEILING_LEAKING', 'Ceiling leaking'), ('KITCHEN__ELECTRICITY', 'Electricity not working'), ('KITCHEN__WIRING_EXPOSED', 'Electric wiring exposed'), ('KITCHEN__OUTLETS', 'Outlets not working'), ('KITCHEN__REFRIGERATOR', 'Refrigerator not working'), ('KITCHEN__REFRIGERATOR_BROKEN', 'Refrigerator broken'), ('KITCHEN__STOVE', 'Stove not working'), ('KITCHEN__STOVE_BROKEN', 'Stove broken'), ('KITCHEN__SINK', 'Cracked sink'), ('KITCHEN__FAUCET_LEAKING', 'Leaky faucet'), ('KITCHEN__NO_FAUCET', 'Faucets not installed'), ('KITCHEN__FAUCET_NOT_WORKING', 'Faucets not working'), ('KITCHEN__WATER_PRESSURE', 'Inadequate water pressure'), ('KITCHEN__PIPES', 'Pipes leaking'), ('KITCHEN__DRAIN', 'Drain stoppage'), ('LIVING_ROOM__MOLD', 'Mold on walls'), ('LIVING_ROOM__WATER', 'Water damage'), ('LIVING_ROOM__PAINT', 'Peeling paint'), ('LIVING_ROOM__WALLS', 'Cracked walls'), ('LIVING_ROOM__LOOSE_FLOOR', 'Loose floor'), ('LIVING_ROOM__BASEBOARDS_DEFECTIVE', 'Baseboards defective'), ('LIVING_ROOM__WINDOW_GLASS_BROKEN', 'Window glass broken'), ('LIVING_ROOM__WINDOW_FRAME_DEFECTIVE', 'Window frame defective'), ('LIVING_ROOM__DOOR', 'Door not working'), ('LIVING_ROOM__RADIATORS', 'Radiators/risers not working'), ('LIVING_ROOM__CEILING', 'Ceiling falling/fell'), ('LIVING_ROOM__CEILING_LEAKING', 'Ceiling leaking'), ('LIVING_ROOM__ELECTRICITY', 'Electricity not working'), ('LIVING_ROOM__WIRING_EXPOSED', 'Electric wiring exposed'), ('LIVING_ROOM__OUTLETS', 'Outlets not working'), ('BATHROOMS__MOLD', 'Mold on walls'), ('BATHROOMS__WATER', 'Water damage'), ('BATHROOMS__PAINT', 'Peeling paint'), ('BATHROOMS__WALLS', 'Cracked walls'), ('BATHROOMS__LOOSE_FLOOR', 'Loose floor'), ('BATHROOMS__BASEBOARDS_DEFECTIVE', 'Baseboards defective'), ('BATHROOMS__WINDOW_GLASS_BROKEN', 'Window glass broken'), ('BATHROOMS__WINDOW_FRAME_DEFECTIVE', 'Window frame defective'), ('BATHROOMS__DOOR', 'Door not working'), ('BATHROOMS__RADIATORS', 'Radiators/risers not working'), ('BATHROOMS__CEILING', 'Ceiling falling/fell'), ('BATHROOMS__CEILING_LEAKING', 'Ceiling leaking'), ('BATHROOMS__ELECTRICITY', 'Electricity not working'), ('BATHROOMS__WIRING_EXPOSED', 'Electric wiring exposed'), ('BATHROOMS__OUTLETS', 'Outlets not working'), ('BATHROOMS__TOILET', 'Toilet not working'), ('BATHROOMS__TOILET_LEAKING', 'Toilet leaking'), ('BATHROOMS__SINK', 'Sink: cracked sink'), ('BATHROOMS__SINK_FAUCET_LEAKING', 'Sink: leaky faucet'), ('BATHROOMS__SINK_NO_FAUCET', 'Sink: faucets not installed'), ('BATHROOMS__SINK_FAUCET_NOT_WORKING', 'Sink: faucets not working'), ('BATHROOMS__SINK_WATER_PRESSURE', 'Sink: low water pressure'), ('BATHROOMS__SINK_PIPES', 'Sink: pipes leaking'), ('BATHROOMS__SINK_DRAIN', 'Sink: drain stoppage'), ('BATHROOMS__TUB', 'Bathtub: cracked tub'), ('BATHROOMS__TUB_FAUCET_LEAKING', 'Bathtub: leaky faucet'), ('BATHROOMS__TUB_NO_FAUCET', 'Bathtub: faucets not installed'), ('BATHROOMS__TUB_FAUCET_NOT_WORKING', 'Bathtub: faucets not working'), ('BATHROOMS__TUB_PIPES', 'Bathtub: pipes leaking'), ('BATHROOMS__TUB_DRAIN', 'Bathtub: drain stoppage'), ('BATHROOMS__SHOWER_MOLD', 'Shower: mold on walls'), ('BATHROOMS__SHOWER_WATER_PRESSURE', 'Shower: wall tiles cracked'), ('BATHROOMS__SHOWER_PIPES', 'Shower: wall tiles missing'), ('BATHROOMS__SHOWER', 'Shower: not working'), ('BATHROOMS__SHOWER_FAUCET_LEAKING', 'Shower: low water pressure'), ('BATHROOMS__SHOWER_NO_FAUCET', 'Shower: leaky shower head'), ('BATHROOMS__SHOWER_DRAIN', 'Shower: drain stoppage'), ('PUBLIC_AREAS__COVID_SANITATION_REQUIRED', 'Needs cleaning due to COVID-19'), ('PUBLIC_AREAS__PAINTING_OVERDUE', 'Painting overdue (3 years)'), ('PUBLIC_AREAS__PAINT', 'Peeling/flaking paint'), ('PUBLIC_AREAS__NO_HEAT', 'No heat'), ('PUBLIC_AREAS__NO_HOT_WATER', 'No hot water'), ('PUBLIC_AREAS__WATER_PRESSURE', 'Inadequate water pressure'), ('PUBLIC_AREAS__RUSTY_WATER', 'Rusty water'), ('PUBLIC_AREAS__WIRING_EXPOSED', 'Electric wiring exposed'), ('PUBLIC_AREAS__ELECTRICAL_CURRENT', 'Weak electrical current'), ('PUBLIC_AREAS__BUGS', 'Bug infestation'), ('PUBLIC_AREAS__PESTS', 'Rats/mice'), ('PUBLIC_AREAS__FUMES', 'Fumes/smoke entering apartment'), ('PUBLIC_AREAS__SMOKE_DETECTORS', 'Broken/no smoke/Co2 detector'), ('PUBLIC_AREAS__WINDOW_GUARDS', 'Window guards missing'), ('PUBLIC_AREAS__WASHING_MACHINE', 'Washing machine not working'), ('PUBLIC_AREAS__DRYER', 'Dryer not working'), ('PUBLIC_AREAS__ILLEGAL_APARTMENTS', 'Illegal apartments in basement'), ('PUBLIC_AREAS__NO_SUPER', 'Inadequate/no super service'), ('PUBLIC_AREAS__RENT_RECEIPTS', 'No rent receipts given'), ('PUBLIC_AREAS__INCOMPLETE_RENT_RECEIPTS', 'Rent receipts incomplete'), ('LANDLORD__RETALIATION', 'Retaliation for seeking repair'), ('LANDLORD__RENT', 'Not receiving rent receipts'), ('LANDLORD__NO_LEASE', 'No lease'), ('LANDLORD__DOCUMENTS', 'False documents'), ('LANDLORD__CONSTRUCTION', 'Illegal construction'), ('LANDLORD__MCI', 'Repeated MCI'), ('LANDLORD__OVERCHARGE', 'Overcharging'), ('LANDLORD__HOLDOVER', 'Holdover cases'), ('LANDLORD__FORCE', 'Using force/threats of force'), ('LANDLORD__STOPPING_SERVICES', 'Stopping essential services'), ('LANDLORD__REMOVING_POSSESSIONS', 'Removing possessions from unit'), ('LANDLORD__CHANGING_LOCKS', 'Changing locks without new key'), ('LANDLORD__BUYOUT', 'Constant buyout demands'), ('LANDLORD__TREATENING_EVICTION', 'False claim eviction threat')], help_text='The issue the user has reported.', max_length=60),
        ),
    ]
