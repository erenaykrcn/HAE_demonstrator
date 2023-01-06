# Generated by Django 4.1.4 on 2023-01-06 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pqc', '0003_alter_custompqcjob_ansatz_entanglement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='custompqcjob',
            name='kl_div',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='custompqcjob',
            name='mw_meas',
            field=models.TextField(blank=True, null=True),
        ),
    ]