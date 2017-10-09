""" forms for Zaboj app """
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    """ form for ordering """
    class Meta:
        """ metadata """
        model = Order
        fields = ['quantity', 'notes']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({'class' : 'form-control custom-select'})
        self.fields['notes'].widget.attrs.update({'class' : 'form-control'})