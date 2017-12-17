"""
Cart admin
"""
from django.contrib import admin
from .models import Cart, CartItem

class CartItemsInline(admin.TabularInline):
    model = CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
    inlines = [CartItemsInline, ]
