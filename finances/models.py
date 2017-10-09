""" Models for finances. """
from django.db import models
from tozd.settings import AUTH_USER_MODEL as User
from users.models import Distributer

class Income(models.Model):
    """ Track all of the incomes. """
    user = models.ForeignKey(User)
    value = models.DecimalField()
    is_donation = models.BooleanField(default=False)
    current_loc = models.ForeignKey(Distributer)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_donation:
            return f'Donacija: {self.value}€ ({self.user})'
        return f'Plačilo: {self.value}€ ({self.user})'
