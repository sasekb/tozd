"""
Models for ZaBoj
"""
from django.apps import apps
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from tozd.settings import AUTH_USER_MODEL as User
from users.models import Distributer

class Vegetable(models.Model):
    """ Veggie model """
    name = models.CharField(max_length=50)
    #user = models.ManyToManyField(User, through='UserPreference')

    def __str__(self):
        return self.name

    class Meta:
        """ Meta data """
        ordering = ('name',)

class Order(models.Model):
    """ Model for orders. """
    choices = [(0.5, '0,5 kg') if i == 0 else (float(i), str(i) + ' kg') for i in range(0, 11)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deprecated_order_user")
    quantity = models.FloatField(choices=choices)
    notes = models.TextField(max_length=400, help_text='Max 400 znakov.', verbose_name="Opombe")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.quantity) + " kg on " + self.created.strftime('%#d. %#m. %Y') \
    + " by " + str(self.user)

    def pretty_date(self):
        """ Returns a formatted date string """
        return self.created.strftime('%#d. %#m. %Y')

    def get_absolute_url(self):
        """ Redirect after edit. """
        return '/u/me'

    def is_processed(self):
        """ Shows if the order is processed in admin """
        ZabojProduction = apps.get_model('management', 'ZabojProduction')
        if ZabojProduction.objects.filter(order=self).exists():
            return True
        return False
    is_processed.boolean = True

    def is_delivered(self):
        """ Shows if the order is delivered in admin """
        ZabojProduction = apps.get_model('management', 'ZabojProduction')
        ZabojDistribution = apps.get_model('management', 'ZabojDistribution')
        package = ZabojProduction.objects.filter(order=self)
        if ZabojDistribution.objects.filter(package=package).exists():
            return True
        return False
    is_delivered.boolean = True

    def action(self):
        """ Next action to do to move the progress along. """
        if not self.is_processed():
            url = reverse('process', kwargs={'order': self.id})
            return format_html(f'<a href="{url}", target="_blank">Process order</a>')
        elif not self.is_delivered():
            ZabojProduction = apps.get_model('management', 'ZabojProduction')
            package = ZabojProduction.objects.filter(order=self).first()
            url = reverse('deliver', kwargs={'package': package.id})
            return format_html(f'<a href="{url}", target="_blank">Deliver order</a>')
        return "No action required"

class Crate(models.Model):
    """ Crate model """
    number = models.PositiveIntegerField()
    at_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    at_distributer = models.ForeignKey(Distributer, null=True, blank=True, on_delete=models.CASCADE)
    in_repairs = models.BooleanField(default=False)

    def __str__(self):
        return '#' + str(self.number)

    def is_home(self):
        """ Shows if the Crate is at the central hub """
        if self.at_user == None and self.at_distributer == None and self.in_repairs == False:
            return True
        return False
    is_home.boolean = True
