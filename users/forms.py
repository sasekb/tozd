"""
Forms for users app
"""
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User


class SignUpForm(UserCreationForm):
    """
    Registration form.
    """
    first_name = forms.CharField(max_length=50, required=False, help_text='Opcijsko.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Opcijsko.')
    email = forms.EmailField(max_length=140, help_text='Zahtevano polje, email mora biti veljaven.')

    class Meta:
        """
        Meta data for the form.
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

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
