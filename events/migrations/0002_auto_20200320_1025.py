# Generated by Django 2.0.4 on 2020-03-20 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pilots', '0002_pilot_nationality'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RaceLaps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lap_time', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lap_number', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RaceResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(blank=True, null=True)),
                ('points', models.IntegerField(blank=True, null=True)),
                ('competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pilots.Pilot')),
                ('laps', models.ManyToManyField(to='events.RaceLaps')),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='competitors',
            field=models.ManyToManyField(to='events.RaceResults'),
        ),
        migrations.AddField(
            model_name='race',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.EventBasic'),
        ),
    ]
