# Generated by Django 4.1.7 on 2023-04-03 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Log_Visualisation_App', '0002_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_name',
            field=models.CharField(default='e1', max_length=255),
            preserve_default=False,
        ),
    ]
