from django.forms import ModelForm
from .models import ZabojProduction

class ProcessOrderForm(ModelForm):
    """ Process orer form. """

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
