# Generated by Django 2.2.14 on 2023-01-07 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pqc', '0007_auto_20230107_1310'),
        ('train', '0006_alter_trainjob_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainjob',
            name='customCircuitJob',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_pqc.CustomPQCJob'),
        ),
        migrations.AlterField(
            model_name='trainjob',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
