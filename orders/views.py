from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpRequest, HttpResponse as HttpResponse
from typing import Any
from orders.models import Order, ItemOrder
from django.contrib import messages
from product.models import Variation, Product
from orders.models import Order, ItemOrder
from utils import omfilters
from django.urls import reverse


class DispatchLoginRequiredMixin(View):  # para onde pagina esta indo
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        if not self.request.user.is_authenticated:  # obriga a tar logado para ter acesso ao pagar!!!!
            return redirect('profile:create')
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        # para so o proprio user ter accso ao seu pagamento
        queryset = queryset.filter(user=self.request.user)

        return queryset


class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'orders/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class SaveOrder(View):
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
        return redirect(reverse("order:pay", kwargs={'pk': order.pk, }))


class Detail(DetailView):
    template_name = 'orders/detail.html'
    model = Order
    pk_url_kwarg = 'pk'  # vais buscar ao kwargs o pk que vem do url
    context_object_name = 'order'

    # def get(self, *args: Any, **kwargs: Any) -> HttpResponse:
    #    return render(self.request, self.template_name)

    # def get_queryset(self, *args, **kwargs):
    #    queryset = super().get_queryset(*args, **kwargs)
    #    # para so o proprio user ter accso ao seu pagamento
    #    id_url = kwargs.get('pk')
    #    queryset = queryset.filter(pk=id_url, user=self.request.user)

    #   return queryset


class ListOrder(DispatchLoginRequiredMixin, ListView):
    model = Order  # model a carregar
    template_name = 'orders/order.html'  # template a renderizar
    # name with objects - in index is page_obj, aqui colide com o paginator
    context_object_name = 'order'
    paginate_by = 9
    ordering = '-id',

    # def get(self, *args: Any, **kwargs: Any) -> HttpResponse:
    #    print(self.queryset)
    #    return render(self.request, self.template_name)

    # se quiser mexer no contexto

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context.update({"user": self.request.user,
    #                     }) nao fazer pq isto nao sei se muda o user mas tira os pedidos
    #     return context
