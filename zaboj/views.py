""" Views for ZaBoj """
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .forms import OrderForm
#from .models import Order

class OrderCreate(LoginRequiredMixin, CreateView):
    form_class = OrderForm
    template_name = 'zaboj/order_form.html'

    def form_valid(self, form):
        """
        Add user on save.
        """
        form.instance.user = self.request.user
        return super(OrderCreate, self).form_valid(form)
