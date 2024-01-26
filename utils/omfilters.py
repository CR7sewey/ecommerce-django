def formata_preco(val):
    return f'E€ {val:.2f}'.replace('.', ',')


def cart_total_qtd(cart):
    return sum([item["quantity"] for item in cart.values()])
