from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Retorna o valor de um dicionário para uma chave especificada."""
    return dictionary.get(key)
