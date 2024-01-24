from django.template import Library

register = Library()

# to load on lista.html


@register.filter
def formata_preco(val):
    return f'E€ {val:.2f}'.replace('.', ',')
