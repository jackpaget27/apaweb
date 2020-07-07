from django.contrib.gis.geoip2 import GeoIP2
import requests
from events.models import *
from django.forms.models import model_to_dict

def get_location(request):

	if not request.session.get('country', None):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
   		
		ip = '216.58.210.46'
		g = GeoIP2()
		country = g.country(ip)
		country = country['country_code']
		response = requests.get('https://restcountries.eu/rest/v2/alpha/' + country)
		geodata = response.json()
		request.session['country'] = country
		request.session['currency'] = geodata['currencies'][0]
		request.session['flag'] = 'flag-icon-' + country.lower()
		request.session.modified = True
		curr = geodata['currencies'][0]		
		response = requests.get('https://api.exchangeratesapi.io/latest?base=GBP&symbols=' + curr['code'])
		exchange_rate  = response.json()
		request.session['exchange_rate'] = exchange_rate['rates'][curr['code']]*1.12

	sale_items = {'Monday':'Mocha 2x1','Tuesday':'Latte 2x1'}
	return {'SALE_ITEMS': sale_items}


def get_championships(request):
	championships = Championship.objects.all().order_by('-id')
	
	return {'menu_championships':championships}