from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from cart.models import Cart, CartItem
from products.models import Variation
from .models import Order, OrderItem, OrderBillingAddress, OrderShippingAddress
from users.models import User, UserBillingAddress, UserShippingAddress, Distributer
from users.forms import UserBillingAddressForm, UserShippingAddressForm, UserPickupMethodForm

class AddressDetailView(FormView, DetailView):
    model = User
    template_name = 'orders/address_detail.html'
    form_class = UserPickupMethodForm

    def get_context_data(self, **kwargs):
        context = super(AddressDetailView, self).get_context_data(**kwargs)
        context['billing_form'] = UserBillingAddressForm()
        context['shipping_form'] = UserShippingAddressForm()
        context['distributers'] = Distributer.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('form-type') == 'billing':
            form = UserBillingAddressForm(request.POST)
        else:
            form = UserShippingAddressForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
        if request.POST.get('copy-address') == 'on':
            form2 = UserShippingAddressForm(request.POST)
            if form2.is_valid():
                obj = form2.save(commit=False)
                obj.user = request.user
                obj.save()
        return HttpResponseRedirect(self.request.path_info)

    def get_object(self):
        """ get object from model class """
        return get_object_or_404(User, pk__iexact=self.request.user.id)

    def get_form_kwargs(self):
        kw = super(AddressDetailView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

def prepare_order(request):
    """
    Prepare the order and return the overview page to confirm order.
    Request looks like: ?distributer=2&bill_addr=1
    """
    distributer_id = request.GET.get('distributer')
    billing_address_id = request.GET.get('bill_addr')
    pickup_method = 2 # this is left in place if we ever decide to have door-to-door deliveries - otherwise it should be deleted
    cart = Cart.objects.get_or_create(user=request.user, processed_to_order=False)[0]
    user_bill_addr = UserBillingAddress.objects.get_or_create(pk=billing_address_id, user=request.user)[0]
    distributer = Distributer.objects.get(pk=distributer_id)

    # Create order
    order = Order()
    order.user = request.user
    order.distributer = distributer
    order.subtotal = cart.subtotal
    order.tax_total = cart.tax_total
    order.total = cart.total
    order.discount_for_returned_package = 0 #TODO implement returned packaging
    order.to_pay = 0 #TODO implement returned packaging
    order.delivery_method = pickup_method
    order.save()

    # create all order items
    for item in cart.cartitem_set.all():
        order_item = OrderItem()
        order_item.order = order
        order_item.item_name = str(item.item)
        order_item.item_price = item.item.price
        order_item.item_quantity = item.quantity
        order_item.item_decimal_quantity = 0 #TODO implement decimal quantity
        order_item.item_unit_of_measure = "kom" #TODO implement decimal quantity
        order_item.item_tax_bracket = item.item.tax_bracket
        order_item.item_subtotal = item.line_subtotal
        order_item.item_tax_total = item.line_tax_total
        order_item.item_total = item.line_tax_total
        if item.item.package_type == None:
             order_item.item_package = None
             order_item.item_package_price = 0
        else:
            order_item.item_package = item.item.package_type.type
            order_item.item_package_price = item.item.package_type.price
        order_item.item_package_subtotal = item.line_package_subtotal
        order_item.item_package_tax_total = item.line_package_tax_total
        order_item.item_package_total = item.line_package_total
        order_item.save()

    billing_address = OrderBillingAddress()
    billing_address.order = order
    billing_address.name = user_bill_addr.name
    billing_address.surname = user_bill_addr.surname
    billing_address.street_name = user_bill_addr.street_name
    billing_address.street_nr = user_bill_addr.street_nr
    billing_address.zip_code = user_bill_addr.zip_code
    billing_address.city = user_bill_addr.city
    billing_address.country = user_bill_addr.country
    billing_address.vat_nr = user_bill_addr.vat_nr
    billing_address.vat_taxpayer = user_bill_addr.vat_taxpayer
    billing_address.save()

    return redirect(reverse('orders_overview', kwargs={'pk': str(order.pk)}))

class OrderDetailView(DetailView):
    model = Order

    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        order = self.get_object()
        order.comment = comment
        order.save()
        return HttpResponse(status=200)


class OrderFinalizeView(TemplateView):
    template_name = 'orders/finalze.html'

    def get(self, request, *args, **kwargs):
        payment_method = request.GET.get('method')
        order = Order.objects.filter(user=request.user).last()
        print(order)
        order.payment_method = payment_method
        order.save()

        cart = Cart.objects.get(processed_to_order=False, user=request.user)
        cart.processed_to_order = True
        cart.save()
        return super(OrderFinalizeView, self).get(request, *args, **kwargs)
