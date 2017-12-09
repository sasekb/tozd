from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class ProductQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.pk)])

class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    active = models.BooleanField(default=True)
    inventory = models.PositiveIntegerField(null=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        return f'{self.product.title} - {self.title}'

    def get_absolute_url(self):
        return self.product.get_absolute_url

@receiver(post_save, sender=Product)
def create_default_variation(instance, **kwargs):
    if instance.variation_set.count() == 0:
        default_variation = Variation()
        default_variation.product = instance
        default_variation.title = "Default"
        default_variation.description = instance.description
        default_variation.price = instance.price
        default_variation.active = instance.active
        default_variation.save()