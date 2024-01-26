from django.urls import include, path
from product import views

app_name = "product"

urlpatterns = [
    path("", views.ListProducts.as_view(), name="lista"),
    path("<slug:slug>", views.DetailProducts.as_view(), name="detail"),
    path("addtocart/", views.AddToCart.as_view(), name="addtocart"),
    path("removefromcart/", views.RemoveFromCart.as_view(),
         name="removefromcart"),
    path("cart/", views.Cart.as_view(),
         name="cart"),
    path("resume/", views.Resume.as_view(), name="resume"),


]
