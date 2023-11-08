from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def kalkulatu_guztira(items):
    guztira = 0
    for item in items:
        guztira += item.unitateak * item.produktua.prezioa
    return "{:.2f}".format(guztira)