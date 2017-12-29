from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from management.models import PackageType

class ProductQueryset(models.query.QuerySet):
    """
    queryset to filter out inactive products and variations
    """
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):
    """
    a model manager thet lets us set the default queryset
    """
    def get_queryset(self):
        return ProductQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

class Product(models.Model):
    """
    Model for products.
    """
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    tax_bracket = models.DecimalField(decimal_places=2, max_digits=4, default="22")
    active = models.BooleanField(default=True)
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE, null=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.pk)])

class Variation(models.Model):
    """
    Model for product variations.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    tax_bracket = models.DecimalField(decimal_places=2, max_digits=4, default="22")
    active = models.BooleanField(default=True)
    inventory = models.PositiveIntegerField(null=True, blank=True)
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE, null=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        if self.title == "Default":
            return self.product.title
        return f'{self.product.title} - {self.title}'

    def get_absolute_url(self):
        """
        returns the absolute URL of the product - variations can't "live" on their own
        """
        return self.product.get_absolute_url

@receiver(post_save, sender=Product)
def create_default_variation(instance, **kwargs):
    """
    When the instance of a Product is saved we should check if a variation exists.
    If not, we should create one with the title "Default".
    """
    if instance.variation_set.count() == 0:
        default_variation = Variation()
        default_variation.product = instance
        default_variation.title = "Default"
        default_variation.description = instance.description
        default_variation.price = instance.price
        default_variation.active = instance.active
        default_variation.package_type = instance.package_type
        default_variation.save()

def image_upload_to(instance, filename):
    print(instance.id)
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = f'{slug}.{file_extension}'
    return f'products/{slug}/{new_filename}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    
    def __str__(self):
        return self.product.title
