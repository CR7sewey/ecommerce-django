from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, HttpRequest
from typing import Any
from orders.models import Order, ItemOrder
from django.contrib import messages
from product.models import Variation, Product
from orders.models import Order, ItemOrder
from utils import omfilters


class Pay(View):
    template_name = 'orders/pay.html'

    def get(self, *args: Any, **kwargs: Any) -> HttpResponse:

        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Please, authenticate!')
            return redirect('profiles:create')

        cart = self.request.session.get('cart')

        if not cart:
            messages.error(self.request, 'Empty cart!')
            return redirect('product:lista')

        cart_keys = [v for v in cart.keys()]
        # actual_products = [Variation.objects.get(
        #    pk=id_var) for id_var in cart_keys]
        bd_variations = list(Variation.objects.select_related('product')
                             .filter(id__in=cart_keys))

        for var in bd_variations:
            vid = str(var.id)  # pq string no cart!
            stock = var.stock

            quantity_cart = cart[vid]['quantity']
            price_unique = cart[vid]['quantity']
            price_unique_promotion = cart[vid]['quantity']

            error_stock = ''

            if stock < quantity_cart:
                cart[vid]['quantity'] = stock
                cart[vid]['price_quantity'] = stock * price_unique
                cart[vid]['price_quantity_promotion'] = stock * \
                    price_unique_promotion

                error_stock = f'At the moment, the stock '\
                    f'available ({stock}) of is lesser than the '\
                    f'quantity chosen ({quantity_cart}). '\
                    f'The quantity was setted to stock number!'
            if error_stock:
                messages.error(self.request, error_stock)
                self.request.session.save()
                return redirect('product:cart')

        # para passar para o context: quanitity_total, price,
        cart = self.request.session.get('cart')
        qtd_total = omfilters.cart_total_qtd(cart)
        value_total = float(omfilters.cart_totals(
            cart).split(' ')[1].replace(",", "."))
        order = Order(user=self.request.user, total=value_total,
                      qtd_total=qtd_total, status='C')
        order.save()

        ItemOrder.objects.bulk_create(
            [ItemOrder(order=order,
                       product=v['product_name'],
                       product_id=v['product_id'],
                       variation=v['variation_name'],
                       variation_id=v['variation_id'],
                       price=v['price_quantity'],
                       promotion_price=v['price_quantity_promotion'],
                       quantity=v['quantity'],
                       image=v['image'],
                       ) for v in cart.values()
             ]

        )  # criar logo todos os objetod do carrinho

        # context = {'qtd_total': qtd_total, 'value_total': value_total}
        del self.request.session['cart']

        # renderizar = render(self.request, self.template_name, context)
        return redirect('order:listorder')


class SaveOrder(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class Detail(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class ListOrder(View):
    def get(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('Lista')
