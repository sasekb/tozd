"""
Production data administration.
"""
from django.contrib import admin
from .filters import DeliveredFilter
from .models import ZabojStorno, ZabojProduction, ZabojDistribution

@admin.register(ZabojProduction)
class ZabojProductionAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
    # list view
    list_display = ['order', 'prepared_by', 'assign_to', 'price', 'created']
    list_editable = ['assign_to', 'price']
    list_filter = (('prepared_by', admin.RelatedOnlyFieldListFilter),
                   'assign_to', 'created', DeliveredFilter)
    search_fields = ['order__user__first_name', 'order__user__last_name', 'order__user__username']
    date_hierarchy = 'created'
    # details view
    readonly_fields = ('created', 'modified', )

@admin.register(ZabojStorno)
class ZabojStornoAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
    # list view
    # details view
    readonly_fields = ('created', 'modified', )

@admin.register(ZabojDistribution)
class ZabojDistributionAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
    # list view
    date_hierarchy = 'created'
    # details view
    readonly_fields = ('created', 'modified', )
