from django.template import Library

register = Library()

# to load on lista.html


@register.filter
def formata_preco(val):
    return f'E€ {val:.2f}'.replace('.', ',')


@register.filter
def cart_total_qtd(cart):
    return sum([item["quantity"] for item in cart.values()])
