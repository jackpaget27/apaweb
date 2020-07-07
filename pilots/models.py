from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from django.db.models import Avg, Count, Min, Sum
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

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
	last_championship_position = models.IntegerField(null=True)

	def get_flag(self):
		nn = self.nationality.code.lower()
		return "flag-icon-" + nn

	def total_points(self, champ):
		if self.raceresults_set.filter(championship=champ).aggregate(Sum('points')).get('points__sum', 0):
			return self.raceresults_set.filter(championship=champ).aggregate(Sum('points')).get('points__sum', 0)
		else:
			return 0

	def best_position(self, champ):
		try:
			return self.raceresults_set.filter(position__gt=0, championship=champ).aggregate(Min('position')).get('position__min', 0)
		except:
			return None

	def driver_podiums(self, champ):
		return self.raceresults_set.filter(position__lte=3, championship=champ).count()

	def championships_entered(self, champ):
		return self.competitors_set.all().count()

	def championship_position(self, champ):
		return self.championshiposition_set.get(championship=champ)

class UserProfile(models.Model):
	telephone_number = PhoneNumberField(null=True)
	mobile_number = PhoneNumberField(null=True)
	email = models.CharField(max_length=250, null=True)
	address_1 = models.CharField(max_length=250, null=True)
	address_2 = models.CharField(max_length=250, null=True)
	address_3 = models.CharField(max_length=250, null=True)
	postcode = models.CharField(max_length=250, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE, null=True)

class MedicalQuestionAnswers(models.Model):
	answer = models.CharField(max_length=25)
	score = models.IntegerField(null=True)

class MedicalQuestions(models.Model):
	question_text = models.TextField()
	question_answers = models.ManyToManyField(MedicalQuestionAnswers)

class MedicalResults(models.Model):
	question = models.ForeignKey(MedicalQuestions, on_delete=models.CASCADE)
	answer = models.ForeignKey(MedicalQuestionAnswers, on_delete=models.CASCADE)

class PilotWaiver(models.Model):
	signed_by = models.CharField(max_length=250)
	signed_on = models.DateField(auto_now_add=True)
	signed_at = models.CharField(max_length=250)
	signed_location = models.CharField(max_length=250)
	waiver_file = models.FileField(upload_to='waiver')

class PilotMedical(models.Model):
	date = models.DateField(auto_now_add=True)
	questions = models.ManyToManyField(MedicalResults)
	score = models.IntegerField()
	outcome = models.BooleanField(default=True)
	signed_by = models.CharField(max_length=250)
	signed_at = models.CharField(max_length=250)
	signed_dob = models.DateField()
	medical_file = models.FileField(upload_to='waiver')

class PilotLicense(models.Model):
	issue = models.DateField()
	expiry = models.DateField()
	medical = models.ForeignKey(PilotMedical, on_delete=models.CASCADE)
	waiver = models.ForeignKey(PilotWaiver, on_delete=models.CASCADE)
	#payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
		

