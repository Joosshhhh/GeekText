from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def replace(value):
    value = str(value)
    return value.replace("-", "/")


@register.filter
def swap(value):
    value = str(value)
    char = list(value)
    char[5] = char[0]
    return ''.join(value)


@register.filter
def gettitle(book):
    return book
