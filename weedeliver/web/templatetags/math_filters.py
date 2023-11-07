from django import template

register = template.Library()


@register.filter(name='sub')
def sub(value, arg):
    value = float(value)
    arg = float(arg)
    return value - arg


@register.filter(name='percent')
def percent(value, arg):
    value = float(value)
    arg = float(arg)
    arg = 100 - arg
    return value * arg / 100


@register.filter(name='multiply')
def multiply(value, arg):
    value = float(value)
    arg = float(arg)
    return value * arg
