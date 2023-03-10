# Generated by Django 4.1.5 on 2023-01-04 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_samples', models.IntegerField(default=200)),
                ('is_binary', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('completed', 'completed'), ('failed', 'failed')], default='pending', max_length=15)),
                ('result_path', models.TextField(blank=True, null=True)),
                ('model', models.CharField(choices=[('HAE', 'HAE'), ('QVC', 'QVC')], default='HAE', max_length=15)),
                ('pqc', models.TextField(default='1')),
                ('precision', models.FloatField(blank=True, null=True)),
                ('recall', models.FloatField(blank=True, null=True)),
                ('f1', models.FloatField(blank=True, null=True)),
                ('precision_cl', models.FloatField(blank=True, null=True)),
                ('recall_cl', models.FloatField(blank=True, null=True)),
                ('f1_cl', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
