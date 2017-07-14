from django import template
from datetime import datetime

register = template.Library()


@register.filter('convert_to_date')
def convert_to_date(date):
    return datetime.strptime(date, '%Y-%m-%d')
