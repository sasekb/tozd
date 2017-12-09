from django.contrib import admin
from .models import Product, Variation

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Admin enchancements"""

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
