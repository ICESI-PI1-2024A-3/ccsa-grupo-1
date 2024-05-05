from django import template
from django.utils import timezone
import pytz 
from datetime import  timedelta
register = template.Library()

@register.filter
def convert_to_database_timezone(time):
    # Get the database timezone
    #database_timezone = timezone.get_current_timezone()
    
    # Convert the time to the database timezone
    #time_with_database_timezone = timezone.localtime(time, database_timezone)
    
    #return time_with_database_timezone
    return time + timedelta(hours=5)