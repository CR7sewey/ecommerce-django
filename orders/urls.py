from django.urls import include, path
from orders import views

app_name = "order"

urlpatterns = [
    path("pay/<int:pk>", views.Pay.as_view(), name="pay"),
    path("saveorder/", views.SaveOrder.as_view(), name="saveorder"),
    path("listorder/", views.ListOrder.as_view(), name="listorder"),
    path("detail", views.Detail.as_view(), name="detail"),

]
