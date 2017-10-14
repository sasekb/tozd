""" Forms for the management app """
from django.forms import ModelForm
from .models import ZabojProduction, ZabojDistribution

class ProcessOrderForm(ModelForm):
    """ Process order form. """

    class Meta:
        """ Meta for the form. """
        model = ZabojProduction
        fields = ['crate', 'distribution_notes', 'enduser_notes', 'assign_to', 'price']

    def __init__(self, *args, **kwargs):
        super(ProcessOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})
        self.fields['crate'].widget.attrs.update({'class' : 'form-control custom-select'})
        self.fields['assign_to'].widget.attrs.update({'class' : 'form-control custom-select'})

class DeliverOrderForm(ModelForm):
    """ Process distribution form. """

    class Meta:
        """ Meta for the form. """
        model = ZabojDistribution
        fields = ['money_received', 'is_extra_donation', 'notes']

    def __init__(self, *args, **kwargs):
        super(DeliverOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})
        self.fields['is_extra_donation'].widget.attrs.update({'class':'form-check-input ml-3', 'type':'checkbox', 'style':'width:24px; height:24px; margin-top:0px'})
