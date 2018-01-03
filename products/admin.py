"""
Shop/products administration.
"""
from itertools import product as carthesian_product

from django.contrib import admin
from django.db.models import Q
from .models import Product, Variation, ProductImage, ProductOptionGroup, ProductOption

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

def make_variations(modeladmin, request, queryset):
    for product in queryset.all():
        options_dict = {}
        for option_group in product.option_groups.all():
            options = []
            for option in option_group.options.all():
                options.append(option)
            options_dict[str(option_group)] = options
        all_variation_options = [dict(zip(options_dict, v)) for v in carthesian_product(*options_dict.values())]
        for variation_options in all_variation_options:
            option_list = list(variation_options.values())
            queryset = Variation.objects.filter(options=option_list[0])
            for option in option_list:
                queryset = queryset.filter(options=option)
            print(queryset)
            if not queryset.exists():
                variation = Variation()
                variation.product = product
                variation.title = " - ".join([option.display_name for option in variation_options.values()])
                variation.description = product.description
                variation.price = product.price
                variation.active = False
                variation.package_type = product.package_type
                variation.save()
                for option in option_list:
                    variation.options.add(option)
make_variations.short_description = 'Naredi vse variacije, ki še ne obstajajo'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
    actions = [make_variations]
    list_display = ['title', 'price']
    inlines = [ProductImageInline, VariationInline]

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    """ Admin enchancements"""

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """ Admin enchancements"""


class ProductOptionInline(admin.TabularInline):
    model = ProductOptionGroup.options.through
    extra = 0

@admin.register(ProductOptionGroup)
class ProductOptionGroupAdmin(admin.ModelAdmin):
    """ Admin enchancements"""
    inlines = [ProductOptionInline,]
    exclude = ['options', ]

admin.site.register(ProductOption)