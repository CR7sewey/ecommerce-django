from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views import View
from product.models import Product, Variation
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpRequest
from typing import Any
from django.db.models.query import QuerySet
from django.contrib import messages
from django.urls import reverse
from profiles.models import UserProfile
from django.db.models import Q  # or
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
        # to destroi cart
        # if self.request.session.get('cart'):
        #    del self.request.session['cart']
        #    self.request.session.save()

        # url anterior à atual!
        http_referer = self.request.META.get('HTTP_REFERER',
                                             reverse('product:lista'))
        vid = self.request.GET.get('vid')  # id da variacao
        if not vid:
            messages.error(self.request, 'Product doesn\'t exist!')
            return redirect(http_referer)

        variation = get_object_or_404(Variation, id=vid)
        variation_stock = variation.stock
        # values to cart
        product = variation.product
        product_id = product.pk
        product_name = product.name
        variation_name = variation.name or ''
        variation_id = vid
        price_unique = variation.price
        price_unique_promotion = variation.promotion_price or price_unique
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.stock < 1:  # if stock = 0
            messages.error(self.request, 'Product doesn\'t exist (stock = 0)!')
            return redirect(http_referer)

        # criamos de se nao existir chave carrinh na sessao do user
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']
        if vid in cart:
            # Variacao existe no carrinho
            quantity_cart = cart[vid]["quantity"]
            quantity_cart += 1
            if variation_stock < quantity_cart:  # not enough stock!
                messages.warning(self.request, f'Stock insuficient for {quantity_cart} '
                                 f'in product {
                                     product_name}. All the stock was added'
                                 f' to your cart ({variation_stock})')
                quantity_cart = variation_stock
            cart[vid]["quantity"] = quantity_cart
            cart[vid]["price_quantity"] = quantity_cart * price_unique
            cart[vid]["price_quantity_promotion"] = quantity_cart * \
                price_unique_promotion

        else:
            # Variacao nao existe no carrinho
            cart[vid] = {
                "product_id": product_id,
                "product_name": product_name,
                "variation_name": variation_name,
                "variation_id": variation_id,
                "price_unique": price_unique,
                "price_unique_promotion": price_unique_promotion,
                "price_quantity": price_unique,
                "price_quantity_promotion": price_unique_promotion,
                "quantity": quantity,
                "slug": slug,
                "image": image,
            }
        self.request.session.save()
        messages.success(self.request, 'Product added to cart!')
        return redirect(http_referer)


class RemoveFromCart(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        http_referer = self.request.META.get('HTTP_REFERER',
                                             reverse('product:lista'))
        vid = self.request.GET.get('vid')  # id da variacao
        if not vid:
            return redirect(http_referer)

        if not self.request.session.get("cart"):
            return redirect(http_referer)

        if vid not in self.request.session["cart"]:
            return redirect(http_referer)

        cart = self.request.session["cart"][vid]
        messages.success(self.request, f"Product {cart["product_name"]}"
                         f"{cart["variation_name"]}"
                         "was removed from your cart!")
        del self.request.session["cart"][vid]
        self.request.session.save()
        return redirect(http_referer)


class Cart(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # Nota: nao preciso de context pois a sessao navega connosco em todas as paginas
        # como se fosse um cookie
        context = {'cart': self.request.session.get('cart', {})}
        return render(self.request, "product/pages/cart.html", context)


class Resume(View):

    def get(self, *args: Any, **kwargs: Any) -> HttpResponse:
        if not self.request.user.is_authenticated:
            return redirect("profiles:create")

        profile = UserProfile.objects.filter(user=self.request.user).exists()
        # verify if exists profile, um utilizador normal é obrigado a ter perfil
        # mas para os admin nao! assim garatne
        if not profile:
            messages.info(
                self.request, 'You need to create a profile in order \
                      to purchase!')
            return redirect("profiles:create")

        # para alguem nao conseguir ver resume se meter diretamente o url na web
        # se nao tiver carrinho
        if not self.request.session.get('cart', {}):
            messages.info(
                self.request, 'You need to add something to cart \
                    to see resume!')
            return redirect("product:lista")

        context = {'user': self.request.user,
                   'cart': self.request.session.get('cart', {})}
        # print(self.request.session.get('cart', {}))
        return render(self.request, 'product/pages/resume.html', context)


class SearchProducts(ListProducts):
    # def __init__(self, **kwargs: Any) -> None:
    #   super().__init__(**kwargs)
    #   self._searched_value = ''

    # def setup(self, request, *args: Any, **kwargs: Any) -> None:
    #   self._searched_value = request.GET.get('search', '').strip()
    #   return super().setup(request, *args, **kwargs)

    # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    # tudo o passado via url esta no kwargs
    #    print("xe")
    # if self._searched_value == '':
    #    return redirect('product:lista')

    # return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        searched_value = self.request.GET.get(
            'search', self.request.session['searched_value']).strip()
        queryset = super().get_queryset(*args, **kwargs)

        if not searched_value:
            return queryset

        # criei sessao para nao mexer na paginacao pq esta a perder o termo search quando mudo!
        self.request.session['searched_value'] = searched_value

        queryset = queryset.filter(Q(name__icontains=searched_value) |
                                   Q(short_description__icontains=searched_value) |
                                   Q(long_description__icontains=searched_value))
        self.request.session.save()
        return queryset
