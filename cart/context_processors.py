"""
This processor provides the item count to every view. This way the cart icon bubble can be updated every time.
"""
from .models import Cart

def item_count(request):
    """
    Finds the cart and returns the context dictionary with the item count.
    """
    try:
        cart = Cart.objects.get(user=request.user, processed_to_order=False)
        return {'cart_items_count': cart.item_count,}
    except Cart.DoesNotExist:
        return {'cart_items_count': 0,}
