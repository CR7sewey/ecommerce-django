from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from product.models import Product
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpRequest
from typing import Any
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


class DetailProducts(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class AddToCart(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class RemoveFromCart(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class Cart(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class Finalise(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')
