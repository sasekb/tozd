from django.contrib import admin
from .models import Order, OrderItem, OrderBillingAddress, OrderShippingAddress


class OrderItemsInline(admin.TabularInline):
    model = OrderItem

class OrderBillingAddressInline(admin.TabularInline):
    model = OrderBillingAddress

class OrderShippingAddressInline(admin.TabularInline):
    model = OrderShippingAddress

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
    inlines = [OrderItemsInline,
               OrderBillingAddressInline,
               OrderShippingAddressInline,
               ]
