# Generated by Django 3.2.12 on 2022-04-20 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laletterbuilder', '0002_laissue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laissue',
            name='letter',
            field=models.ForeignKey(help_text='The letter reporting the issue.', on_delete=django.db.models.deletion.CASCADE, related_name='laletterbuilder_laissue', to='laletterbuilder.habitabilityletter'),
        ),
        migrations.AlterField(
            model_name='laissue',
            name='value',
            field=models.CharField(choices=[('HEALTH__MOLD__BEDROOM', 'Mold'), ('HEALTH__MOLD__LIVING_ROOM', 'Mold'), ('HEALTH__MOLD__DINING_ROOM', 'Mold'), ('HEALTH__MOLD__BATHROOM', 'Mold'), ('HEALTH__MOLD__KITCHEN', 'Mold'), ('HEALTH__MOLD__HALLWAY', 'Mold'), ('HEALTH__MOLD__COMMON_AREAS', 'Mold'), ('HEALTH__MOLD__NA', 'Mold'), ('HEALTH__PEELING_PAINT__BEDROOM', 'Peeling paint'), ('HEALTH__PEELING_PAINT__LIVING_ROOM', 'Peeling paint'), ('HEALTH__PEELING_PAINT__DINING_ROOM', 'Peeling paint'), ('HEALTH__PEELING_PAINT__BATHROOM', 'Peeling paint'), ('HEALTH__PEELING_PAINT__KITCHEN', 'Peeling paint'), ('HEALTH__PEELING_PAINT__HALLWAY', 'Peeling paint'), ('HEALTH__PEELING_PAINT__COMMON_AREAS', 'Peeling paint'), ('HEALTH__PEELING_PAINT__NA', 'Peeling paint'), ('HEALTH__RODENT_INFESTATION__BEDROOM', 'Rodent infestation'), ('HEALTH__RODENT_INFESTATION__LIVING_ROOM', 'Rodent infestation'), ('HEALTH__RODENT_INFESTATION__DINING_ROOM', 'Rodent infestation'), ('HEALTH__RODENT_INFESTATION__BATHROOM', 'Rodent infestation'), ('HEALTH__RODENT_INFESTATION__KITCHEN', 'Rodent infestation'), ('HEALTH__RODENT_INFESTATION__HALLWAY', 'Rodent infestation'), ('HEALTH__RODENT_INFESTATION__COMMON_AREAS', 'Rodent infestation'), ('HEALTH__RODENT_INFESTATION__NA', 'Rodent infestation'), ('HEALTH__BUG_INFESTATION__BEDROOM', 'Bug infestation'), ('HEALTH__BUG_INFESTATION__LIVING_ROOM', 'Bug infestation'), ('HEALTH__BUG_INFESTATION__DINING_ROOM', 'Bug infestation'), ('HEALTH__BUG_INFESTATION__BATHROOM', 'Bug infestation'), ('HEALTH__BUG_INFESTATION__KITCHEN', 'Bug infestation'), ('HEALTH__BUG_INFESTATION__HALLWAY', 'Bug infestation'), ('HEALTH__BUG_INFESTATION__COMMON_AREAS', 'Bug infestation'), ('HEALTH__BUG_INFESTATION__NA', 'Bug infestation'), ('HEALTH__SMOKE_CO2_DETECTOR__BEDROOM', 'Smoke or carbon monoxide detector'), ('HEALTH__SMOKE_CO2_DETECTOR__LIVING_ROOM', 'Smoke or carbon monoxide detector'), ('HEALTH__SMOKE_CO2_DETECTOR__DINING_ROOM', 'Smoke or carbon monoxide detector'), ('HEALTH__SMOKE_CO2_DETECTOR__BATHROOM', 'Smoke or carbon monoxide detector'), ('HEALTH__SMOKE_CO2_DETECTOR__KITCHEN', 'Smoke or carbon monoxide detector'), ('HEALTH__SMOKE_CO2_DETECTOR__HALLWAY', 'Smoke or carbon monoxide detector'), ('HEALTH__SMOKE_CO2_DETECTOR__COMMON_AREAS', 'Smoke or carbon monoxide detector'), ('HEALTH__SMOKE_CO2_DETECTOR__NA', 'Smoke or carbon monoxide detector'), ('HEALTH__TRASH_CANS__BROKEN', 'Trash cans'), ('HEALTH__TRASH_CANS__NOT_ENOUGH', 'Trash cans'), ('HEALTH__TRASH_CANS__OTHER', 'Trash cans'), ('UTILITIES__DEFECTIVE_ELECTRICITY__BEDROOM', 'Defective electricity'), ('UTILITIES__DEFECTIVE_ELECTRICITY__LIVING_ROOM', 'Defective electricity'), ('UTILITIES__DEFECTIVE_ELECTRICITY__DINING_ROOM', 'Defective electricity'), ('UTILITIES__DEFECTIVE_ELECTRICITY__BATHROOM', 'Defective electricity'), ('UTILITIES__DEFECTIVE_ELECTRICITY__KITCHEN', 'Defective electricity'), ('UTILITIES__DEFECTIVE_ELECTRICITY__HALLWAY', 'Defective electricity'), ('UTILITIES__DEFECTIVE_ELECTRICITY__COMMON_AREAS', 'Defective electricity'), ('UTILITIES__DEFECTIVE_ELECTRICITY__NA', 'Defective electricity'), ('UTILITIES__SHUT_OFF__WATER', 'Utilities shut off'), ('UTILITIES__SHUT_OFF__GAS', 'Utilities shut off'), ('UTILITIES__SHUT_OFF__ELECTRICITY', 'Utilities shut off'), ('UTILITIES__SHUT_OFF__OTHER', 'Utilities shut off'), ('UTILITIES__WATER_LEAK__BATHROOM', 'Water leak'), ('UTILITIES__WATER_LEAK__KITCHEN', 'Water leak'), ('UTILITIES__WATER_LEAK__LAUNDRY_ROOM', 'Water leak'), ('UTILITIES__WATER_LEAK__COMMON_AREAS', 'Water leak'), ('UTILITIES__WATER_LEAK__NA', 'Water leak'), ('UTILITIES__DEFECTIVE_PLUMBING__BEDROOM', 'Defective plumbing'), ('UTILITIES__DEFECTIVE_PLUMBING__LIVING_ROOM', 'Defective plumbing'), ('UTILITIES__DEFECTIVE_PLUMBING__DINING_ROOM', 'Defective plumbing'), ('UTILITIES__DEFECTIVE_PLUMBING__BATHROOM', 'Defective plumbing'), ('UTILITIES__DEFECTIVE_PLUMBING__KITCHEN', 'Defective plumbing'), ('UTILITIES__DEFECTIVE_PLUMBING__HALLWAY', 'Defective plumbing'), ('UTILITIES__DEFECTIVE_PLUMBING__COMMON_AREAS', 'Defective plumbing'), ('UTILITIES__DEFECTIVE_PLUMBING__NA', 'Defective plumbing'), ('UTILITIES__NO_HOT_WATER__BATHROOM', 'No hot water'), ('UTILITIES__NO_HOT_WATER__KITCHEN', 'No hot water'), ('UTILITIES__NO_HOT_WATER__LAUNDRY_ROOM', 'No hot water'), ('UTILITIES__NO_HOT_WATER__COMMON_AREAS', 'No hot water'), ('UTILITIES__NO_HOT_WATER__NA', 'No hot water'), ('BUILDING_AND_SAFETY__HOLES__BEDROOM', 'Holes'), ('BUILDING_AND_SAFETY__HOLES__LIVING_ROOM', 'Holes'), ('BUILDING_AND_SAFETY__HOLES__DINING_ROOM', 'Holes'), ('BUILDING_AND_SAFETY__HOLES__BATHROOM', 'Holes'), ('BUILDING_AND_SAFETY__HOLES__KITCHEN', 'Holes'), ('BUILDING_AND_SAFETY__HOLES__HALLWAY', 'Holes'), ('BUILDING_AND_SAFETY__HOLES__COMMON_AREAS', 'Holes'), ('BUILDING_AND_SAFETY__HOLES__NA', 'Holes'), ('BUILDING_AND_SAFETY__BROKEN_WINDOWS__BEDROOM', 'Broken/defective windows'), ('BUILDING_AND_SAFETY__BROKEN_WINDOWS__LIVING_ROOM', 'Broken/defective windows'), ('BUILDING_AND_SAFETY__BROKEN_WINDOWS__DINING_ROOM', 'Broken/defective windows'), ('BUILDING_AND_SAFETY__BROKEN_WINDOWS__BATHROOM', 'Broken/defective windows'), ('BUILDING_AND_SAFETY__BROKEN_WINDOWS__KITCHEN', 'Broken/defective windows'), ('BUILDING_AND_SAFETY__BROKEN_WINDOWS__HALLWAY', 'Broken/defective windows'), ('BUILDING_AND_SAFETY__BROKEN_WINDOWS__COMMON_AREAS', 'Broken/defective windows'), ('BUILDING_AND_SAFETY__BROKEN_WINDOWS__NA', 'Broken/defective windows'), ('BUILDING_AND_SAFETY__INSECURE_LOCKS__FRONT_DOOR', 'Broken/insecure locks'), ('BUILDING_AND_SAFETY__INSECURE_LOCKS__BACK_DOOR', 'Broken/insecure locks'), ('BUILDING_AND_SAFETY__INSECURE_LOCKS__BUILDING_MAIN_ENTRANCE', 'Broken/insecure locks'), ('BUILDING_AND_SAFETY__INSECURE_LOCKS__BUILDING_PARKING_ENTRANCE', 'Broken/insecure locks'), ('BUILDING_AND_SAFETY__INSECURE_LOCKS__NA', 'Broken/insecure locks'), ('BUILDING_AND_SAFETY__FAULTY_DOORS__FRONT_DOOR', 'Faulty doors'), ('BUILDING_AND_SAFETY__FAULTY_DOORS__BACK_DOOR', 'Faulty doors'), ('BUILDING_AND_SAFETY__FAULTY_DOORS__BUILDING_MAIN_ENTRANCE', 'Faulty doors'), ('BUILDING_AND_SAFETY__FAULTY_DOORS__BUILDING_PARKING_ENTRANCE', 'Faulty doors'), ('BUILDING_AND_SAFETY__FAULTY_DOORS__NA', 'Faulty doors'), ('BUILDING_AND_SAFETY__UNSAFE_STAIRS__BUILDING_MAIN_ENTRANCE', 'Unsafe/broken stairs and/or railing'), ('BUILDING_AND_SAFETY__UNSAFE_STAIRS__BUILDING_EXIT', 'Unsafe/broken stairs and/or railing'), ('BUILDING_AND_SAFETY__UNSAFE_STAIRS__FLOOR_LEVEL', 'Unsafe/broken stairs and/or railing'), ('BUILDING_AND_SAFETY__UNSAFE_STAIRS__OTHER', 'Unsafe/broken stairs and/or railing')], help_text='The issue the letter is reporting.', max_length=100),
        ),
    ]
