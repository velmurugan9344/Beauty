# Generated by Django 5.0.6 on 2025-03-11 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='is_cancelled',
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('Canceled', 'Canceled')], default='Scheduled', max_length=10),
        ),
    ]
