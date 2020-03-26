# Generated by Django 2.0.4 on 2020-03-20 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_eventbasic_event_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boat_number', models.IntegerField()),
                ('boat_registration', models.CharField(max_length=250)),
                ('boat_image', models.FileField(upload_to='boats')),
            ],
        ),
        migrations.AddField(
            model_name='raceresults',
            name='boat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Boat'),
        ),
    ]
