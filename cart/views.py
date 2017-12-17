"""
Views for the Shopping Cart app.
"""
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, render

from products.models import Variation
from .models import Cart, CartItem

class CartView(View):
    """
    Base view for the cart.
    """
    model = Cart
    template_name = "cart/cart_view.html"

    def get(self, request):
        """
        Implementing the GET method response.
        """
        #TODO: ali implementiramo cart za neprijavljene uporabnike?
        item_pk = request.GET.get('item')
        quantity = request.GET.get('qty', 1)
        delete = request.GET.get('rm')
        cart, created = Cart.objects.get_or_create(user=request.user)
        if created:
            cart.save()
        if item_pk:
            item = get_object_or_404(Variation, pk=item_pk)
            cart_item = CartItem.objects.get_or_create(cart=cart, item=item)[0]
            if delete:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
        context = {
            "cart": cart
        }
        if request.is_ajax():
            data = {
                "message": "Success!",
                "item": item_pk,
                "lineTotal": format(cart_item.line_total, '.2f'),
                "total": format(cart.total, '.2f'),
                "taxTotal": format(cart.tax_total, '.2f'),
                "subtotal": format(cart.subtotal, '.2f'),
            }
            return JsonResponse(data) 

        template = self.template_name
        return render(request, template, context)
