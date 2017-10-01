"""
Admin for the zaboj orders
"""
from django.contrib import admin
from .filters import ProcessedFilter, DeliveredFilter, CrateHomeFilter
from .models import Order, Vegetable, Crate

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Create admin views for Orders"""
    #Order.is_processed.boolean = True
    # list views
    list_display = ['user', 'quantity', 'created', 'is_processed', 'is_delivered', 'action']
    list_filter = ['created', ProcessedFilter, DeliveredFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    date_hierarchy = 'created'
    # details view
    readonly_fields = ('created', 'modified', )

def return_crate(modeladmin, request, queryset):
    """ Use special action to bulk return Crates to the central hub. """
    queryset.update(
        at_user = None,
        at_distributer = None)
return_crate.short_description = 'Return crates to central hub.'

def send_to_service(modeladmin, request, queryset):
    """ Use special action to bulk send Crates to the service. """
    queryset.update(in_repairs = True)
send_to_service.short_description = 'Send crates to service.'

def receive_from_service(modeladmin, request, queryset):
    """ Use special action to bulk send Crates to the service. """
    queryset.update(in_repairs = False)
receive_from_service.short_description = 'Receive crates from service.'

@admin.register(Crate)
class CrateAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
    # list view
    actions = [return_crate, send_to_service, receive_from_service]
    list_display = ['number', 'at_user', 'at_distributer', 'in_repairs', 'is_home']
    search_fields = ['number']
    list_filter = (('at_user', admin.RelatedOnlyFieldListFilter),
                   ('at_distributer', admin.RelatedOnlyFieldListFilter),
                   'in_repairs', CrateHomeFilter)

admin.site.register(Vegetable)
