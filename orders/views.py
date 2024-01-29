from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, HttpRequest
from typing import Any
from orders.models import Order, ItemOrder


class Pay(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class SaveOrder(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class Detail(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')
