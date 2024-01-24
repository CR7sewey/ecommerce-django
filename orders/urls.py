from django.urls import include, path
from orders import views

app_name = "order"

urlpatterns = [
    path("pay/", views.Pay.as_view(), name="pay"),
    path("finishorder/", views.FinishOrder.as_view(), name="finishorder"),
    path("detail/<int:pk>", views.Detail.as_view(), name="detail"),

]
