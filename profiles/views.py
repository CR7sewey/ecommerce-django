from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpRequest, HttpResponse
from typing import Any
from . import models
from . import forms

# Create your views here.


class BaseProfile(View):
    template_name = 'profiles/create.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        user_form = forms.UserForm(data=request.POST or None)
        profile_form = forms.ProfileForm(
            data=request.POST or None)  # ,instance=)

        if request.user.is_authenticated:

            self.context = {'userform': forms.UserForm(data=request.POST or None,
                                                       user=request.user,
                                                       instance=request.user),
                            'profileform': profile_form}

            self.renderizar = render(
                request, self.template_name, self.context)

        else:
            self.context = {'userform': user_form,
                            'profileform': profile_form}

            self.renderizar = render(
                request, self.template_name, self.context)

        return super().setup(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return self.renderizar


class Create(BaseProfile):
    def post(self, *args: Any, **kwargs: Any):
        # form = self.context["userform"]
        # if form.is_valid():  # true if all validations are passed!
        # new_user = form.save(commit=False)  # commit dont allow saving!
        # contact.show = False
        #  new_user.save()

        return self.renderizar


class Update(BaseProfile):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class Login(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class Logout(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')
