# Generated by Django 4.1.7 on 2023-04-03 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Log_Visualisation_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocel_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Log_Visualisation_App.ocellog')),
            ],
        ),
    ]
