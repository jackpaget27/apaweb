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
		return 0

