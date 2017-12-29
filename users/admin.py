"""
Adim for the users app
"""
from django.contrib import admin
from .models import User, Distributer, UserBillingAddress, UserShippingAddress
from zaboj.models import Order

class OrdersInline(admin.TabularInline):
    """ Shows orders on user's admin page """
    model = Order
    classes = ['collapse']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ User admin enhancements. """
    # list view
    list_display = ['first_name', 'last_name', 'district', 'is_union_member']
    list_editable = ['district',]
    # detail view
    fieldsets = (
        ('Account info', {
            'fields': (('username', 'email'),)
        }),
        ('User info', {
            'classes': ('extrapretty', ),
            'fields': (('first_name', 'last_name'),
                       ('address', 'city'),
                       'district',
                       'phone_nr'
            )
        }),
        ('Delivery method', {
            'fields': ('pickup_method',)
        }),
        ('Preferences', {
            'fields': (('likes', 'dislikes'))
        }),
        ('Dates', {
            'classes': ('collapse',),
            'fields': (('date_joined', 'last_login'))
        }),
        ('Administration', {
            'classes': ('collapse',),
            'fields': (('is_superuser', 'user_permissions'),
                       ('is_staff', 'groups'),
                       ('is_active', 'password')
            )
        }),
        ('Union membership', {
            'fields': ('is_union_member',)
        })
    )
    radio_fields = {'pickup_method': admin.HORIZONTAL}
    filter_horizontal = ['likes', 'dislikes']
    inlines = [OrdersInline]
    save_on_top = True
    save_as = True

@admin.register(UserBillingAddress)
class UserBillingAddressAdmin(admin.ModelAdmin):
    model = UserBillingAddress

@admin.register(UserShippingAddress)
class UserShippingAddressAdmin(admin.ModelAdmin):
    model = UserShippingAddress

@admin.register(Distributer)
class DistributerAdmin(admin.ModelAdmin):
    """ Distributer admin enhancements. """
    # list view
    list_display = ['user', 'district', 'main']
    list_editable = ['district', 'main']
    list_editable = ['district', 'main']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    # detail view
