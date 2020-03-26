# Generated by Django 2.0.4 on 2020-03-20 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pilots', '0002_pilot_nationality'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilot',
            name='championship_position',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pilot',
            name='championships_entered',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
