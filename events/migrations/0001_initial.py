# Generated by Django 2.0.4 on 2020-03-19 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventBasic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(max_length=250)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('event_proposed_date', models.CharField(blank=True, max_length=250, null=True)),
                ('event_cover', models.FileField(upload_to='event-covers')),
            ],
        ),
    ]
