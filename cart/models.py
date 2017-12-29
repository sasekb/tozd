"""
Models for the shopping cart.
"""
from django.db import models
from products.models import Variation
from tozd.settings import AUTH_USER_MODEL as User
from tozd.settings import VAT_BRACKET_HIGH

class Cart(models.Model):
    """
    Shopping cart contains the order.
    """
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    items = models.ManyToManyField(
        Variation,
        through='CartItem',
        through_fields=('cart', 'item', 'quantity'),
    )
    processed_to_order = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} ({self.created})'

    @property
    def total(self):
        """
        Returns the total price of the cart
        """
        products = sum([float(line.line_total) for line in self.cartitem_set.all()])
        package = sum([float(line.line_package_total) for line in self.cartitem_set.all()])
        return products + package

    @property
    def tax_total(self):
        """
        Returns the total tax value of the cart
        """
        products = sum([float(line.line_tax_total) for line in self.cartitem_set.all()])
        package = sum([float(line.line_package_tax_total) for line in self.cartitem_set.all()])
        return products + package

    @property
    def subtotal(self):
        """
        Returns the total price of the cart without the tax.
        """
        products = sum([float(line.line_subtotal) for line in self.cartitem_set.all()])
        package = sum([float(line.line_package_subtotal) for line in self.cartitem_set.all()])
        print(products,package)
        return products + package

    @property
    def item_count(self):
        """
        Returns the count of items in the cart
        """
        return sum([item.quantity for item in self.cartitem_set.all()])

class CartItem(models.Model):
    """
    Items in the Shopping cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.item.title

    @property
    def line_total(self):
        """
        Return the total price of one item in the cart.
        """
        return int(self.quantity) * float(self.item.price)

    @property
    def line_tax_total(self):
        """
        Return the total price of one item in the cart.
        """
        products = int(self.quantity) * float(self.item.price) * float(self.item.tax_bracket) / 100
        return products

    @property
    def line_subtotal(self):
        """
        Return the total price of one item in the cart.
        """
        return int(self.quantity) * float(self.item.price) * (1 - float(self.item.tax_bracket) / 100)

    @property
    def line_package_total(self):
        """
        Return the total price of the packaging for one item in the cart.
        """
        if self.item.package_type == None:
            return 0
        return int(self.quantity) * float(self.item.package_type.price)

    @property
    def line_package_subtotal(self):
        """
        Return the subtotal (no VAT) of the packaging for one item in the cart.
        """
        if self.item.package_type == None:
            return 0
        return int(self.quantity) * float(self.item.package_type.price) * (1 - VAT_BRACKET_HIGH)

    @property
    def line_package_tax_total(self):
        """
        Return the total tax value of the packaging for one item in the cart.
        """
        if self.item.package_type == None:
            return 0
        return int(self.quantity) * float(self.item.package_type.price) * VAT_BRACKET_HIGH
