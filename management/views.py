"""
Views for order management.
"""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from tozd.settings import PRICE_ZABOJ
from orders.models import Order
from users.models import Distributer
from zaboj.models import Crate
from .forms import ProcessOrderForm, DeliverOrderForm
from .models import ZabojProduction, ZabojDistribution

class OrdersList(PermissionRequiredMixin, ListView):
    """ View all orders and filter them. """
    permission_required = 'is_staff'
    model = Order
    template_name = 'management/orders.html'

    def get_queryset(self):
        filter_val = self.request.GET.get('show_processed', None)
        if filter_val:
            queryset = Order.objects.all().order_by('-created')
        else:
            queryset = Order.objects.exclude(id__in=ZabojProduction.objects.values_list('order')).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        """ Additional context. """
        context = super(OrdersList, self).get_context_data(**kwargs)
        context['show_processed'] = self.request.GET.get('show_processed', False)
        if context['show_processed']:
            context['zaboj_productions'] = ZabojProduction.objects.values_list('order_id', flat=True)
        return context

class ProcessOrder(CreateView):
    """ Fill out production details """
    form_class = ProcessOrderForm
    template_name = 'management/fillout_order.html'

    def get_context_data(self):
        """ pass user preferences """
        context = super(ProcessOrder, self).get_context_data()
        order = get_object_or_404(Order, id=self.kwargs.get('order'))
        context['ordered_by'] = order.user
        return context

    def get_form(self):
        """ get form to change fields """
        form = super(ProcessOrder, self).get_form()
        form.fields['crate'].queryset = Crate.objects.filter(at_user=None).filter(at_distributer=None).filter(in_repairs=False)
        return form

    def get_initial(self):
        """ set initial state """
        order = get_object_or_404(Order, id=self.kwargs.get('order'))
        distributer = Distributer.objects.filter(district=order.user.district).first()
        return {
            'assign_to': distributer,
            'price':order.quantity*PRICE_ZABOJ
        }

    def form_valid(self, form):
        """ if the saved form is valid save everything you need to save """
        # move crate to the distributer
        crate = get_object_or_404(Crate, id=form.instance.crate.id)
        crate.at_distributer = form.instance.assign_to
        crate.save()
        form.instance.order = get_object_or_404(Order, id=self.kwargs.get('order'))
        form.instance.prepared_by = self.request.user
        return super(ProcessOrder, self).form_valid(form)

class UpdateProcessOrder(UpdateView):
    """ Update production details """
    form_class = ProcessOrderForm
    template_name = 'management/fillout_order.html'

    def get_context_data(self):
        """ pas user preferences """
        context = super(UpdateProcessOrder, self).get_context_data()
        order = get_object_or_404(Order, id=self.kwargs.get('order'))
        context['ordered_by'] = order.user
        return context

    def get_form(self):
        """ get form to change fields """
        form = super(UpdateProcessOrder, self).get_form()
        form.fields['crate'].queryset = Crate.objects.filter(at_user=None).filter(at_distributer=None).filter(in_repairs=False) | Crate.objects.filter(id=self.object.crate.id)
        return form

    def get_object(self):
        """ get the object we want to edit """
        return get_object_or_404(ZabojProduction, order__id=self.kwargs.get('order'))

    def form_valid(self, form):
        """ if the saved form is valid save everything you need to save """
        # move crate to the distributer
        crate = get_object_or_404(Crate, id=form.instance.crate.id)
        crate.at_distributer = form.instance.assign_to
        crate.save()
        form.instance.order = get_object_or_404(Order, id=self.kwargs.get('order'))
        form.instance.prepared_by = self.request.user
        return super(UpdateProcessOrder, self).form_valid(form)

class DeliveriesList(PermissionRequiredMixin, ListView):
    """ View all orders and filter them. """
    permission_required = 'is_staff'
    model = ZabojProduction
    template_name = 'management/deliveries.html'

    def get_queryset(self):
        queryset = ZabojProduction.objects
        show_processed = self.request.GET.get('show_processed', None)
        show_all = self.request.GET.get('show_all', None)
        user = get_object_or_404(Distributer, user=self.request.user)
        if not show_all:
            queryset = queryset.filter(assign_to=user)
        if show_processed:
            queryset = queryset.order_by('-created')
        else:
            queryset = queryset.exclude(id__in=ZabojDistribution.objects.values_list('package')).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        """ Additional context. """
        context = super(DeliveriesList, self).get_context_data(**kwargs)
        context['show_processed'] = self.request.GET.get('show_processed', False)
        context['show_all'] = self.request.GET.get('show_all', False)
        if context['show_processed']:
            context['zaboj_deliveries'] = ZabojDistribution.objects.values_list('package_id', flat=True)
        return context

class DeliveriesAllList(PermissionRequiredMixin, ListView):
    """
    View all orders and filter them.

    THIS FUNCTIONALITY IS REDUNDANT
    We will delete it once we've made the DeliveriesList more secure!
    """
    permission_required = 'is_staff'
    model = ZabojProduction
    template_name = 'management/deliveries.html'

    def get_queryset(self):
        filter_val = self.request.GET.get('show_processed', None)
        if filter_val:
            queryset = ZabojProduction.objects.all().order_by('-created')
        else:
            queryset = ZabojProduction.objects.exclude(id__in=ZabojDistribution.objects.values_list('package')).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        """ Additional context. """
        context = super(DeliveriesAllList, self).get_context_data(**kwargs)
        context['show_processed'] = self.request.GET.get('show_processed', False)
        context['all'] = True
        return context

class DeliverOrder(CreateView):
    """ Edit the delivery status. """
    form_class = DeliverOrderForm
    template_name = 'management/fillout_delivery.html'

    def get_context_data(self):
        """ pass notes for the distributer """
        context = super(DeliverOrder, self).get_context_data()
        package = get_object_or_404(ZabojProduction, id=self.kwargs.get('package'))
        context['package'] = package
        return context

    def get_initial(self):
        package = get_object_or_404(ZabojProduction, id=self.kwargs.get('package'))
        return {
            'money_received': package.price,
        }

    def form_valid(self, form):
        package = get_object_or_404(ZabojProduction, id=self.kwargs.get('package'))
        # move crate to the end user
        crate = package.crate
        order = package.order
        crate.at_distributer = None
        crate.at_user = order.user
        crate.save()
        # save package and assign delivery to currently logged-in user
        form.instance.package = package
        form.instance.delivered_by = self.request.user
        # create money trail

        return super(DeliverOrder, self).form_valid(form)
