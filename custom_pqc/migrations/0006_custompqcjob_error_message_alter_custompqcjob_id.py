# Generated by Django 4.1.4 on 2023-01-06 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pqc', '0005_auto_20230106_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='custompqcjob',
            name='error_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='custompqcjob',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]