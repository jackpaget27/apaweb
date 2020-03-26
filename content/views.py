from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
#from aviationmanagement.decorators import locked_screen
from datetime import datetime
from django.contrib import messages
from django.urls import reverse

from . import models
from events.models import *
from pilots.models import *

def index(request):

	events = EventBasic.objects.all().order_by('-id')[0:4]
	pilots = Pilot.objects.filter(display=True).order_by('championship_position')
	context = {
		'events' : events,
		'pilots' : pilots,
	}
	template = loader.get_template('content/index.html')
	return HttpResponse(template.render(context, request))


def championship(request, the_slug):
	event = EventBasic.objects.get(slug=the_slug)
	competitors = event.competitors.all().order_by('final_position')

	context = {
		'event' : event,
		'competitors' : competitors,
	}

	if event.completed == True:
		template = loader.get_template('content/championship.html')
	else:
		template = loader.get_template('content/championship-future.html')

	return HttpResponse(template.render(context, request))

def championship_racers(request):
	pilots = Pilot.objects.all().order_by('championship_position')

	context = {
		'pilots' : pilots,
	}

	template = loader.get_template('content/drivers.html')
	return HttpResponse(template.render(context, request))

def championship_standings(request):
	pilots = Pilot.objects.all().order_by('championship_position')
	events = EventBasic.objects.filter(completed=True)

	context = {
		'pilots' : pilots,
		'events' : events,
	}
	
	template = loader.get_template('content/drivers-championship.html')
	return HttpResponse(template.render(context, request))

def reset_championship_postions(request):
	for pilot in Pilot.objects.all():
		pos = 1
		if not pilot.total_points():
			pos = Pilot.objects.all().count()
		else:
			for p in Pilot.objects.all():
				if not p == pilot and p.total_points():
					if p.total_points() > pilot.total_points():
						pos=pos+1

			pilot.championship_position = pos
			pilot.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

