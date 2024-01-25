from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic.list import ListView
from django.views import View
from product.models import Product, Variation
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpRequest
from typing import Any
from django.db.models.query import QuerySet
from django.contrib import messages
# Create your views here.

# Create your views here.
# posts = list(range(1000))

PER_PAGE = 9


class ListProducts(ListView):
    model = Product  # model a carregar
    template_name = 'product/pages/lista.html'  # template a renderizar
    # name with objects - in index is page_obj, aqui colide com o paginator
    context_object_name = 'products'
    ordering = '-id',
    paginate_by = PER_PAGE
    # paginator_class = Paginator  # - default
    queryset = Product.objects.all()


class DetailProducts(DetailView):
    model = Product
    template_name = 'product/pages/product.html'
    context_object_name = 'product'
    slug_field = 'slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    # este metodo pq queremso uma http response!
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        get_object_or_404(Product, slug=self.kwargs.get("slug"))
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        # desnecsasrio
        # queryset = queryset.filter(slug=self.kwargs.get("slug"))
        return queryset


class AddToCart(View):  # como é view temos de escrever metodos get e/ou post
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # messages.error(self.request, 'Erro')
        # url anterior à atual!
        http_referer = self.request.META.get('HTTP_REFERER',
                                             reverse('product:lista'))
        vid = self.request.GET.get('vid')
        if not vid:
            messages.error(self.request, 'Product doesn\'t exist!')
            return redirect(http_referer)

        variation = get_object_or_404(Variation, id=vid)

        # criamos de se nao existir chave carrinh na sessao do user
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']
        if vid in cart:
            # TODO: Variacao existe no carrinho
            pass
        else:
            # TODO: Variacao nao existe no carrinho
            pass

        return HttpResponse(variation.name)


class RemoveFromCart(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class Cart(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class Finalise(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')
