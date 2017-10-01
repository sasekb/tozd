""" Filters for management app admin """
from django.contrib import admin
from .models import ZabojDistribution

class DeliveredFilter(admin.SimpleListFilter):
    """ Delivered filter for the ZabojProduction admin """
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
            return queryset.filter(id__in=ZabojDistribution.objects.values_list('package'))
        if self.value() == 'no':
            return queryset.exclude(id__in=ZabojDistribution.objects.values_list('package'))
