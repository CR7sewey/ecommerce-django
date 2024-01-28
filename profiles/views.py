from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views import View
from django.http import HttpRequest, HttpResponse
from typing import Any
from . import models
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import copy

# Create your views here.


class BaseProfile(View):
    template_name = 'profiles/create.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)

        # pq o carro de compras apaga qunado se muda senha do user no update
        # assim guardamos numa variavel!
        self.cart = copy.deepcopy(request.session.get('cart', {}))

        user_form = forms.UserForm(data=request.POST or None)
        profile_form = forms.ProfileForm(
            data=request.POST or None)  # ,instance=)
        self.perfil = None

        if request.user.is_authenticated:
            self.perfil = models.UserProfile.objects.filter(
                user=request.user).first()
            # print(self.perfil)
            # print(request.user, models.UserProfile.objects.all())

            self.context = {'userform': forms.UserForm(data=request.POST or None,
                                                       user=request.user,
                                                       instance=request.user),
                            'profileform': forms.ProfileForm(
                                data=request.POST or None,
                instance=self.perfil)}

        else:
            self.context = {'userform': user_form,
                            'profileform': profile_form}

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'profiles/update.html'

        self.renderizar = render(
            request, self.template_name, self.context)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return self.renderizar


class Create(BaseProfile):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if not self.userform.is_valid():  # or not self.profileform.is_valid()
            return self.renderizar
        print("ENTREIIIIIIIIIIIIII - so dps de dados enviaddos no forms!")
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password1')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # if user logado!
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            user.username = username

            if password:  # se mudar perco a sessao e consequentemente o carrinho de compras
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # PERFIL/OUNAO DE UM USER JA LOGADO
            if not self.perfil:  # usuario logado mas sem perfil!
                # profile = self.profileform.save(commit=False)
                # profile.user = user
                # profile.save()
                # messages.success(self.request, 'New user created!')
                self.profileform.cleaned_data['user'] = user
                profile = models.UserProfile(**self.profileform.cleaned_data)
                profile.save()
            else:  # para atualizar!
                profile = self.profileform.save(commit=True)
                profile.user = user  # so para garantir
                profile.save()

        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(self.request, 'New user created!')

        # para torcar o id de sessao e passar o id para a proxima sessao
        if password:
            autentica = authenticate(
                self.request, username=user.username, password=password)

            if autentica:  # loga o usuario apos alterar a senha
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()
        return self.renderizar


class Update(BaseProfile):  # made in create!
    def post(self, *args: Any, **kwargs: Any):

        return self.renderizar


class Login(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')


class Logout(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse('pagar')
