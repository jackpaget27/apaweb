from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from django.db.models import Avg, Count, Min, Sum
from datetime import date


class Pilot(models.Model):
	first_name = models.CharField(max_length=250)
	last_name = models.CharField(max_length=250)
	dob = models.DateField(null=True, blank=True)
	weight = models.IntegerField(null=True)
	height = models.IntegerField(null=True)
	bio = models.TextField(null=True)
	facebook = models.CharField(max_length=250, null=True, blank=True)
	instagram = models.CharField(max_length=250, null=True, blank=True)
	youtube = models.CharField(max_length=250, null=True, blank=True)
	website = models.CharField(max_length=250, null=True, blank=True)
	profile_image = models.FileField(upload_to='pilots/profile', null=True)
	nationality = CountryField()
	display = models.BooleanField(default=True)
	championship_position = models.IntegerField(null=True)

	def get_flag(self):
		nn = self.nationality.code.lower()
		return "flag-icon-" + nn

	def total_points(self):
		if self.raceresults_set.all().aggregate(Sum('points')).get('points__sum', 0):
			return self.raceresults_set.all().aggregate(Sum('points')).get('points__sum', 0)
		else:
			return 0

	def best_position(self):
		try:
			return self.raceresults_set.filter(position__gt=0).aggregate(Min('position')).get('position__min', 0)
		except:
			return None

	def driver_podiums(self):
		return self.raceresults_set.filter(position__lte=3).count()

	def championships_entered(self):
		return self.competitors_set.all().count()

