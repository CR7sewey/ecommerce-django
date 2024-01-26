from typing import Dict


def formata_preco(val):
    return f'E€ {val:.2f}'.replace('.', ',')


def cart_total_qtd(cart):
    return sum([item["quantity"] for item in cart.values()])


def cart_totals(cart):
    total = 0
    for linha in cart.values():
        quantity = int(linha.get("quantity"))
        value = int(linha.get("price_unique_promotion")
                    if linha.get("price_unique_promotion") else linha.get("price_unique"))
        total += quantity*value
    return formata_preco(total)
