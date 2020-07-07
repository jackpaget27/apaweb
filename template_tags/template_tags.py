from django import template
from events.models import *
from pilots.models import *

register = template.Library()

@register.simple_tag(name='get_driver_result')
def get_driver_result(event_id, driver_id, race_number):
	event = EventBasic.objects.get(id=event_id)
	return event.competitor_result(driver_id, race_number)

@register.simple_tag(name='get_driver_event')
def get_driver_event(event_id, driver_id):
	pilot = Pilot.objects.get(id=driver_id)
	event = EventBasic.objects.get(id=event_id)
	try:
		result = event.competitors.filter(entrant=pilot)[0]
		return result.final_points
	except:
		return "-"

@register.simple_tag(name='get_driver_race')
def get_driver_race(event_id, driver_id, race_number):
	try:
		pilot = Pilot.objects.get(id=driver_id)
		event = EventBasic.objects.get(id=event_id)
		race = event.race_set.get(race_number=race_number)
		result = race.competitors.get(competitor=pilot)

		return result.points

	except: 
		return "-"

@register.simple_tag(name='get_championship_points')
def get_championship_points(championship_id, driver_id):
	pilot = Pilot.objects.get(id=driver_id)
	champ = Championship.objects.get(id=championship_id)
	try:
		result = pilot.total_points(champ)
		return result
	except:
		return "-"

@register.simple_tag(name='get_championship_best')
def get_championship_best(championship_id, driver_id):
	pilot = Pilot.objects.get(id=driver_id)
	champ = Championship.objects.get(id=championship_id)
	try:
		result = pilot.best_position(champ)
		if result:
			return result
		else:
			return "-"
	except:
		return "-"

@register.simple_tag(name='get_championship_podiums')
def get_championship_podiums(championship_id, driver_id):
	pilot = Pilot.objects.get(id=driver_id)
	champ = Championship.objects.get(id=championship_id)
	try:
		result = pilot.driver_podiums(champ)
		return result
	except:
		return "-"

@register.simple_tag(name='get_championship_entered')
def get_championship_entered(championship_id, driver_id):
	pilot = Pilot.objects.get(id=driver_id)
	champ = Championship.objects.get(id=championship_id)
	try:
		result = pilot.championships_entered(champ)
		return result
	except:
		return "-"


@register.simple_tag(name='get_championship_position')
def get_championship_position(championship_id, driver_id):
	pilot = Pilot.objects.get(id=driver_id)
	championship = Championship.objects.get(id=championship_id)
	champ = ChampionshipPosition.objects.get(championship=championship, pilot=pilot)
	result = champ.championship_position
	if result:
		return result
	else:
		return "-"

@register.simple_tag(name='get_championship_colour')
def get_championship_colour(championship_id, driver_id):
	pilot = Pilot.objects.get(id=driver_id)
	championship = Championship.objects.get(id=championship_id)
	champ = ChampionshipPosition.objects.get(championship=championship, pilot=pilot)
	result = champ.championship_position
	if result == 1:
		return "color: #D4AF37;"
	elif result == 2:
		return "color: #C0C0C0;"
	elif result == 3:
		return "color: #cd7f32;"
	else:
		return ""

