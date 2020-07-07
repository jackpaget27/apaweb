from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from django.template.defaultfilters import slugify
from django.db.models import Avg, Count, Min, Sum
from datetime import date
from pilots.models import *

class Boat(models.Model):
	boat_number = models.IntegerField()
	boat_registration = models.CharField(max_length=250)
	boat_image = models.FileField(upload_to='boats')

	def number_of_races(self):
		return self.raceresults_set.all().count()

	def boat_pilots(self):
		return self.competitors_set.distinct("entrant")

	def location(self):
		competitors = self.competitors_set.all()
		events = EventBasic.objects.filter(competitors__boat=self)
		return events

class Competitors(models.Model):
	entrant = models.ForeignKey(Pilot, on_delete=models.CASCADE)
	boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
	final_points = models.IntegerField(null=True)
	final_position = models.IntegerField(null=True)

class Sponsors(models.Model):
	name = models.CharField(max_length=250)
	logo = models.FileField(upload_to='sponsors')

class EventBasic(models.Model):
	event_title = models.CharField(max_length=250)
	event_date = models.DateField(null=True, blank=True)
	event_proposed_date = models.CharField(max_length=250, null=True, blank=True)
	event_cover = models.FileField(upload_to='event-covers')
	event_country = CountryField(null=True)
	event_description = models.TextField(null=True)
	competitors = models.ManyToManyField(Competitors)
	slug = models.SlugField(unique=True, null=True)
	sponsors = models.ManyToManyField(Sponsors)
	completed = models.BooleanField(default=False)

	def past_event(self):
		if self.event_date < date.today():
			return True
		elif self.event_date > date.today():
			return False

	def get_flag(self):
		nn = self.event_country.code.lower()
		return "flag-icon-" + nn

	def competitors_display(self):
		return self.competitors.filter(entrant__display=True).order_by('entrant__championship_position')

	def races(self):
		return self.race_set.all().order_by('race_number')

	def competitor_result(self, competitor, race):
		pilot = Pilot.objects.get(id=competitor)
		race = Race.objects.get(event=self, race_number=race)
		race_results = race.competitors.get(competitor__id=competitor)
		return race_results.points

class Championship(models.Model):
	name = models.CharField(max_length=250)
	events = models.ManyToManyField(EventBasic)
	slug = models.SlugField(unique=True, null=True)
	pilot = models.ManyToManyField(Pilot)

class ChampionshipPosition(models.Model):
	championship = models.ForeignKey(Championship, null=True, on_delete=models.CASCADE)
	championship_position = models.IntegerField(null=True)
	pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)

class RaceLaps(models.Model):
	lap_time = models.DecimalField(decimal_places=2, max_digits=10)
	lap_number = models.IntegerField(null=True, blank=True)

class RaceResults(models.Model):
	competitor = models.ForeignKey(Pilot, on_delete=models.CASCADE)
	boat = models.ForeignKey(Boat, on_delete=models.CASCADE, null=True)
	position = models.IntegerField(null=True, blank=True)
	points = models.IntegerField(null=True, blank=True)
	laps = models.ManyToManyField(RaceLaps)
	championship = models.ForeignKey(Championship, null=True, blank=True, on_delete=models.CASCADE)

class Race(models.Model):
	event = models.ForeignKey(EventBasic, on_delete=models.CASCADE)
	race_number = models.IntegerField()
	competitors = models.ManyToManyField(RaceResults)

class Documentation(models.Model):
	document_name = models.CharField(max_length=250)
	document_version = models.CharField(max_length=250)
	document_link = models.CharField(max_length=250)
	document_published = models.DateField(auto_now_add=True)
	document_active = models.BooleanField()