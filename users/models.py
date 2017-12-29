""" Models for the users app. """
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """
    Extending the default User model.
    Iz registra:
    IME	PRIIMEK	    REGIJA	    KRAJ	    SKUPNOST
    NASLOV	        MAIL	    TELEFON	    VEZA
    PREVZEMNI REŽIM	ROTACIJA_K	ROTACIJA_Z	ČLAN
    """
    phone_re = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                              message='Telefonska mora biti v formatu "+999999999". \
                                       Dovoljenih do 15 znakov.')

    address = models.CharField(max_length=120, blank=True, null=True,
                               help_text='Ulica in hišna številka.')
    city = models.CharField(max_length=50, blank=True, null=True,
                            help_text='Ime kraja (brez poštne številke).')
    district = models.CharField(max_length=50, blank=True, null=True,
                                help_text='Ime četrtne skupnosti (npr. "Bežigrad"). Lahko prazno.')
    phone_nr = models.CharField(max_length=15, validators=[phone_re], blank=True, null=True,
                                help_text='Format: +38611111111')
    pickup_method = models.IntegerField(choices=[(1, 'Dostava na dom'),
                                                 (2, 'Prevzem pri distributerju'),
                                                 (3, 'Leteči')],
                                        help_text='1. Dostavmo na dom (+1€). \
                                                   2. Prevzem v svoji četrti/kraju. \
                                                   3. Prevzem na poti po dogovoru z distributerjem.'
                                        , null=True)
    is_union_member = models.BooleanField(default=False)
    likes = models.ManyToManyField('zaboj.Vegetable', related_name='%(class)s_likes')
    dislikes = models.ManyToManyField('zaboj.Vegetable', related_name='%(class)s_dislikes')

    def get_absolute_url(self):
        """ Redirect after edit. """
        return '/u/me'

    def __str__(self):
        return f'{self.last_name}, {self.first_name} ({self.username})'

class UserBillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    street_name = models.CharField(max_length=120)
    street_nr = models.CharField(max_length=10)
    zip_code = models.PositiveIntegerField()
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    vat_nr = models.PositiveIntegerField(blank=True, null=True)
    vat_taxpayer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.surname}, {self.street_name} {self.street_nr}'

class UserShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    street_name = models.CharField(max_length=120)
    street_nr = models.CharField(max_length=10)
    zip_code = models.PositiveIntegerField()
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.name} {self.surname}, {self.street_name} {self.street_nr}'

class Distributer(models.Model):
    """
    Model for the distributers. Fields:
    USER (User)    DISTRICT (Char)    MAIN (Bool)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    main = models.BooleanField()

    def __str__(self):
        return str(self.user) + " (" + str(self.district) + ")"
