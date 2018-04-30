"""
views for users app
"""
# from django.shortcuts import render
#from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms.fields import CharField
from django.http import HttpResponse #, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView, CreateView
from django.urls import reverse
from zaboj.models import Vegetable
from .forms import SignUpForm, UserPreferenceForm
from .models import User

def logout_view(request):
    logout(request)
    return redirect("index")

def test_view(request, ttt):
    """
    A view to test shit.
    """
    from django.contrib.auth import get_user_model
    UserTest = get_user_model()
    print(str(UserTest.username))
    print(request)
    return HttpResponse(ttt)

class UserHome(LoginRequiredMixin, DetailView):
    """
    home view for user - order history, pending orders, payments, customization of the profile, etc
    """
    model = User
    queryset = User.objects.all()
    template_name = "users/home.html"
    login_url = '/login/'
    success_url = "/u/"

    def get_object(self):
        """
        get object from model class
        """
        requested_user = self.kwargs.get('username')
        loggedin_user = self.request.user.username
        if str(requested_user) == str(loggedin_user) or requested_user == 'me':
            requested_user = loggedin_user
            return get_object_or_404(User, username__iexact=requested_user, is_active=True)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(UserHome, self).get_context_data(**kwargs)
        #user = self.request.user.get_profile()
        context['likes'] = self.request.user.likes.all()
        context['dislikes'] = self.request.user.dislikes.all()
        print(self.request.user.likes.all())
        print(type(self.request.user.likes.all()))
        context['remaining_veggies'] = Vegetable.objects.all().exclude(id__in=[x.id for x in self.request.user.likes.all() | self.request.user.dislikes.all()])
        return context



class UserEdit(LoginRequiredMixin, UpdateView):
    """
    Edit basic information about user
    """
    model = User
    fields = ['first_name', 'last_name', 'address', 'city', 'district', 'phone_nr', 'pickup_method']
    template_name_suffix = '_update_form'

    def get_object(self):
        """ get object from model class """
        return get_object_or_404(User, id__iexact=self.request.user.id)

class SignUpView(FormView):
    model = User
    form_class = SignUpForm
    success_url = '/'

    template_name = 'users/signup.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(self.request, user)
        return super(SignUpView, self).form_valid( form)


# def signup(request):
#     """
#     render the registration form
#     """
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('/u/me')
#     else:
#         form = SignUpForm()
#     return render(request, 'users/signup.html', {'form': form})



class EditPreferences(LoginRequiredMixin, UpdateView):
    """ edit user data """
    model = User
    form_class = UserPreferenceForm
    template_name_suffix = '_preference_form'

    def get_object(self):
        """ get object from model class """
        return get_object_or_404(User, id__iexact=self.request.user.id)
