from django.db import models
from tozd.settings import AUTH_USER_MODEL as User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    subtotal = models.DecimalField(decimal_places=2, max_digits=8)
    tax_total = models.DecimalField(decimal_places=2, max_digits=8)
    total = models.DecimalField(decimal_places=2, max_digits=8)
    discount_for_returned_package = models.DecimalField(decimal_places=2, max_digits=8)
    to_pay = models.DecimalField(decimal_places=2, max_digits=8)
    delivery_method = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    payment_method = models.IntegerField(choices=((1, "Gotovina"), (2, "Predračun"), (3, "Predplačilo")), default=1)
    finalized = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    arrived = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} ({self.created})'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=120)
    item_price = models.DecimalField(decimal_places=2, max_digits=8)
    item_quantity = models.PositiveIntegerField(blank=True, null=True)
    item_decimal_quantity = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    item_unit_of_measure = models.CharField(max_length=20, blank=True, null=True)
    item_tax_bracket = models.DecimalField(decimal_places=2, max_digits=4)
    item_subtotal = models.DecimalField(decimal_places=2, max_digits=8)
    item_tax_total = models.DecimalField(decimal_places=2, max_digits=8)
    item_total = models.DecimalField(decimal_places=2, max_digits=8)
    item_package = models.CharField(max_length=120, blank=True, null=True)
    item_package_price = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    item_package_subtotal = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    item_package_tax_total = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    item_package_total = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)

    def __str__(self):
        return f'{self.order}: {self.item_name}'

class OrderBillingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    street_name = models.CharField(max_length=120)
    street_nr = models.CharField(max_length=10)
    zip_code = models.PositiveIntegerField()
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    company_name = models.CharField(max_length=120, blank=True, null=True)
    vat_nr = models.PositiveIntegerField(blank=True, null=True)
    vat_taxpayer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.surname}, {self.street_name} {self.street_nr}'

class OrderShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    street_name = models.CharField(max_length=120)
    street_nr = models.CharField(max_length=10)
    zip_code = models.PositiveIntegerField()
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.name} {self.surname}, {self.street_name} {self.street_nr}'
