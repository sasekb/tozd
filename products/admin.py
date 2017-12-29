"""
Shop/products administration.
"""
from django.contrib import admin
from .models import Product, Variation, ProductImage

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
    list_display = ['title', 'price']
    inlines = [ProductImageInline, VariationInline]

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    """ Admin enchancements"""

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
