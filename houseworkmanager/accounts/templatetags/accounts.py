import calendar
import datetime
from datetime import date

from django import template
from django.utils import timezone

register = template.Library()

@register.inclusion_tag('accounts/users_point.html')
def users_point(user, **kwargs):
    if 'year' in kwargs:
        year = kwargs['year']
    else:
        year = timezone.now().year
    if 'month' in kwargs:
        month = kwargs['month']
    else:
        month = timezone.now().month
    startdate = date(year, month, 1)
    enddate = date(year, month, calendar.monthrange(year, month)[1])
    table = []
    for user in user.group.users.all():
        table.append({
            'user': user,
            'total_point': user.calc_point(),
            'monthly_point': user.calc_point(startdate=startdate, enddate=enddate)
        })
    return {'table': table, 'user': user}

@register.inclusion_tag('accounts/users_point_form.html')
def users_point_form(user, **kwargs):
    if 'year' in kwargs:
        year = kwargs['year']
    else:
        year = timezone.now().year
    if 'month' in kwargs:
        month = kwargs['month']
    else:
        month = timezone.now().month
    startdate = date(year, month, 1)
    enddate = date(year, month, calendar.monthrange(year, month)[1])
    table = []
    for user in user.group.users.all():
        table.append({
            'user': user,
            'total_point': user.calc_point(),
            'monthly_point': user.calc_point(startdate=startdate, enddate=enddate)
        })
    return {'table': table, 'user': user}