from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
import pycountry
from datetime import datetime
from django.contrib import messages
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.gis.geoip2 import GeoIP2
import requests
from . import models
from events.models import *
from pilots.models import *

def get_client_location(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    ip = '87.113.97.255'
    g = GeoIP2()
    country = g.country(ip)
    country = country['country_code']
    response = requests.get('https://restcountries.eu/rest/v2/alpha/' + country)
    geodata = response.json()
    print(geodata)
    return {
        'currencies': geodata['currencies'][0],
        'country': country
    }

def index(request):

	events = EventBasic.objects.filter(completed=False).order_by('-id')[0:4]
	pilots = Pilot.objects.filter(display=True).order_by('last_name')

	championships = Championship.objects.all().order_by('-id')[1]
	champ_events = championships.events.all()

	context = {
		'events' : events,
		'pilots' : pilots,
		'champ_events' : champ_events,
		'championship' : championships,
	}
	template = loader.get_template('content/index.html')
	return HttpResponse(template.render(context, request))


def championship_index(request, the_slug):

	championship = Championship.objects.get(slug=the_slug)
	championship_standings = ChampionshipPosition.objects.filter(championship=championship).order_by('championship_position')

	context = {
		'championship' : championship,
		'championship_standings' : championship_standings,
	}

	template = loader.get_template('content/championship-index.html')
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
	pilots = Pilot.objects.all().order_by('last_name')
	championships = Championship.objects.all().order_by('-id')[1]
	context = {
		'pilots' : pilots,
		'championship' : championships,
	}

	template = loader.get_template('content/drivers.html')
	return HttpResponse(template.render(context, request))

def championship_standings(request, see_full=None):
	pilots = Pilot.objects.all().order_by('championship_position')
	events = EventBasic.objects.filter(completed=True).order_by('id')

	context = {
		'pilots' : pilots,
		'events' : events,
	}
	
	if see_full == True:
		template = loader.get_template('content/drivers-full-results.html')
	else:
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

def team(request):

	context = {

	}
	
	template = loader.get_template('content/team.html')
	return HttpResponse(template.render(context, request))

def documentation(request):

	docs = Documentation.objects.filter(document_active=True)

	context = {

		'docs' : docs,

	}

	template = loader.get_template('content/documentation.html')
	return HttpResponse(template.render(context, request))

def corporate(request):

	context = {

	}
	
	template = loader.get_template('content/corporate.html')
	return HttpResponse(template.render(context, request))

def about(request):

	boats = Boat.objects.filter(boat_number__gt=0)

	context = {

		'boats': boats,

	}
	
	template = loader.get_template('content/about.html')
	return HttpResponse(template.render(context, request))

def contact(request):

	if request.method == "POST":
		name = request.POST.get("name")
		email = request.POST.get("email")
		subject = request.POST.get("company")
		message = request.POST.get("request")



	context = {


	}
	
	template = loader.get_template('content/contact.html')
	return HttpResponse(template.render(context, request))


def join(request):
	paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "10000000.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn'))
    }

    # Create the instance.
	form = PayPalPaymentsForm(initial=paypal_dict)

	context = {
		'form' : form,
	}
	
	template = loader.get_template('content/join_us.html')
	return HttpResponse(template.render(context, request))

def training_centres(request):

	context = {

	}

	template = loader.get_template('content/training_centres.html')
	return HttpResponse(template.render(context, request))

def news(request):

	context = {

	}

	template = loader.get_template('content/news.html')
	return HttpResponse(template.render(context, request))
