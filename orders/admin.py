from django.contrib import admin
from orders.models import ItemOrder, Order

# Register your models here.


@admin.register(ItemOrder)
class ItemOrderAdmin(admin.ModelAdmin):
    ...

# TO put variation inline in admin (in product)


class ItemOrderInline(admin.TabularInline):
    model = ItemOrder
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = ItemOrderInline,
