# Generated by Django 4.1.4 on 2023-01-06 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pqc', '0002_custompqcjob_ansatz_custompqcjob_ansatz_entanglement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompqcjob',
            name='ansatz_entanglement',
            field=models.TextField(blank=True, default='full', null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='ansatz_entanglement_blocks',
            field=models.TextField(blank=True, default='cx', null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='ansatz_reps',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='ansatz_rotation_blocks',
            field=models.TextField(blank=True, default="['ry', 'rz']", null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='ansatz_skip_final_rotation_layer',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='ansatz_skip_unentangled_qubits',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='ansatz_su2_gates',
            field=models.TextField(blank=True, default="['ry', 'y']", null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='encoder_alpha',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='encoder_entanglement',
            field=models.TextField(blank=True, default='full', null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='encoder_entanglement_blocks',
            field=models.TextField(blank=True, default='cx', null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='encoder_paulis',
            field=models.TextField(blank=True, default="['Z', 'ZZ']", null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='encoder_reps',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='encoder_rotation_blocks',
            field=models.TextField(blank=True, default="['ry', 'rz']", null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='encoder_skip_final_rotation_layer',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
