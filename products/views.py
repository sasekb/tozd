"""
Views for products -> store.
"""

from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product, Variation

class ProductDetailView(DetailView):
    model = Product

    def get(self, request, **kwargs):
        if request.is_ajax():
            product = request.GET.get('product')
            options = request.GET.get('options', '').split(',')
            queryset = Variation.objects.filter(product=product)
            for option in options:
                queryset = queryset.filter(options=option)
            if not queryset.exists():
                return JsonResponse({"message": "Kombinacija ne obstaja."})
            if queryset.count() > 1:
                return JsonResponse({"message": "Izdelek ni unikatno določen z izbranimi opcijami."})
            variation = queryset.first()
            if not variation.active:
                return JsonResponse({"message": "Kombinacija ni aktivna."})
            data = {
                "message": "Izdelek uspešno najden.",
                "id": variation.pk,
                "price": variation.price,
            }
            return JsonResponse(data)
        else:
            return super(ProductDetailView, self).get(request, **kwargs)

class ProductListView(ListView):
    model = Product
