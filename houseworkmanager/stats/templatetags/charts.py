import datetime
from django import template

register = template.Library()

@register.inclusion_tag('stats/chart.html')
def show_chart(chart):
    chart_dict = {
        'table': chart.table,
        'title': chart.title(),
        'js_path': chart.js_path()
    }
    return {'chart_dict': chart_dict}
