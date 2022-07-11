from pyexpat import model
from random import choices
from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.urls import reverse
from django_countries.fields import CountryField
# Create your models here.
CATEGORY_CHOICE = (
('S', 'Shirt'),
('SW', 'SportWear'),
('OW', 'Out Wear')
)
LABEL_CHOICES = (
    ('p', 'primary'),
    ('s', 'secondary'),
    ('d', 'danger')
)
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)   
    category = models.CharField(choices = CATEGORY_CHOICE, max_length=2)
    label = models.CharField(choices = LABEL_CHOICES,max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("core:product-detail", kwargs={'slug':self.slug})
    def add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'slug':self.slug})
    def remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'slug':self.slug})
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def get_total_item_price(self):
        total_quantity= self.item.price*self.quantity
        return total_quantity
    def get_total_item_discountprice(self):
        total_quantity=self.item.discount_price*self.quantity
        return total_quantity   
    def get_amount_saved(self):
        amount_saved = self.get_total_item_price() - self.get_total_item_discountprice()
        return amount_saved
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discountprice()
        return self.get_total_item_price()
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple = True)
    zip_code = models.CharField(max_length=100)
