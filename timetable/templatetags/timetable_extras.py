from django import template

register = template.Library()

@register.filter
def get_day(grid, day):
    return grid.get(day, {})

@register.filter
def get_hour(day_dict, hour):
    return day_dict.get(hour, None)