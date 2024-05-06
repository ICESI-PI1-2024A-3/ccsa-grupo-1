from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def convert_to_database_timezone(time):
    return time + timedelta(hours=5)
