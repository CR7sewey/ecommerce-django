from django.contrib import admin
from .models import Product, Variation

# Register your models here.


# TO put variation inline in admin (in product)
class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = VariationInline,


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    ...
