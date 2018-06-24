"""
Forms for users app
"""
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, UserBillingAddress, UserShippingAddress


class SignUpForm(UserCreationForm):
    """
    Registration form.
    """
    
    class Meta:
        """
        Meta data for the form.
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

class UserPreferenceForm(ModelForm):
    """
    User preference form - for users.
    """
    fields = ('likes', 'dislikes',)

    class Meta:
        """ Meta for the form. """
        model = User
        fields = ('likes', 'dislikes',)
    
    def __init__(self, *args, **kwargs):
        super(UserPreferenceForm, self).__init__(*args, **kwargs)
        self.fields['likes'].widget.attrs.update({'class' : 'form-control custom-select', 'style': 'height: 100%;'})
        self.fields['dislikes'].widget.attrs.update({'class' : 'form-control custom-select', 'style': 'height: 100%;'})

class UserPickupMethodForm(ModelForm):
    """
    User preference form - for users.
    """
    fields = ('pickup_method',)

    class Meta:
        """ Meta for the form. """
        model = User
        fields = ('pickup_method',)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(UserPickupMethodForm, self).__init__(*args, **kwargs)
        self.fields['pickup_method'].initial = request.user.pickup_method

class UserBillingAddressForm(ModelForm):
    """
    Form to add new user address for billing
    """
    fields = ('name', 'surname', 'street_name', 'street_nr', 'zip_code', 'city', 'country', 'vat_nr', 'vat_taxpayer', )

    class Meta:
        """ Meta for the form. """
        model = UserBillingAddress
        fields = ('name', 'surname', 'street_name', 'street_nr', 'zip_code', 'city', 'country', 'vat_nr', 'vat_taxpayer', )

class UserShippingAddressForm(ModelForm):
    """
    Form to add new user address for shipping
    """
    fields = ('name', 'surname', 'street_name', 'street_nr', 'zip_code', 'city', 'country', )

    class Meta:
        """ Meta for the form. """
        model = UserShippingAddress
        fields = ('name', 'surname', 'street_name', 'street_nr', 'zip_code', 'city', 'country', )
