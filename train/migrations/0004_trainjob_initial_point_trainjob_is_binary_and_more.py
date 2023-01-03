# Generated by Django 4.1.4 on 2023-01-03 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0003_alter_trainjob_id_alter_trainjob_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainjob',
            name='initial_point',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trainjob',
            name='is_binary',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='trainjob',
            name='max_iter',
            field=models.IntegerField(default=100),
        ),
    ]