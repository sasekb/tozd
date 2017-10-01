from django.contrib import admin
from .models import Order
from management.models import ZabojDistribution, ZabojProduction

class ProcessedFilter(admin.SimpleListFilter):
    # Human-readable title
    title = ('process status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'processed'

    def lookups(self, request, model_admin):
        """ Shown in filter """
        return (
            ('yes', ('Processed')),
            ('no', ('Waiting for process')),
        )

    def queryset(self, request, queryset):
        """ Returns the filtered queryset based on the value provided """
        if self.value() == 'yes':
            return queryset.filter(id__in=ZabojProduction.objects.values_list('order'))
        if self.value() == 'no':
            return queryset.exclude(id__in=ZabojProduction.objects.values_list('order'))

class DeliveredFilter(admin.SimpleListFilter):
    # Human-readable title
    title = ('delivery status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'delivered'

    def lookups(self, request, model_admin):
        """ Shown in filter """
        return (
            ('yes', ('Delivered')),
            ('no', ('Waiting for delivery')),
        )

    def queryset(self, request, queryset):

        """ Returns the filtered queryset based on the value provided """
        if self.value() == 'yes':
            return queryset.filter(zabojproduction__id__in=ZabojDistribution.objects.values_list('package'))
        if self.value() == 'no':
            return queryset.exclude(zabojproduction__id__in=ZabojDistribution.objects.values_list('package'))

class CrateHomeFilter(admin.SimpleListFilter):
    # Human-readable title
    title = ('home location')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'location'

    def lookups(self, request, model_admin):
        """ Shown in filter """
        return (
            ('home', ('Home')),
            ('away', ('Away')),
        )

    def queryset(self, request, queryset):

        """ Returns the filtered queryset based on the value provided """
        if self.value() == 'home':
            return queryset.filter(at_user=None).filter(at_distributer=None).filter(in_repairs=False)
        if self.value() == 'away':
            return queryset.exclude(at_user=None) | queryset.exclude(at_distributer=None) | queryset.exclude(in_repairs=False)
