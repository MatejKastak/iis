from django import template

register = template.Library()

@register.simple_tag
def access_dict(dictionary, dictionary_key):
    return dictionary.get(dictionary_key, {})
