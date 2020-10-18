from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone


class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    compleated = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def shipping(self):
        order_items = self.orderitem_set.all()
        shipping = False
        for item in order_items:
            if item.product.digital is False:
                shipping = True

        return shipping


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        url = self.image.url
        if not url:
            url = ''
        return url


class OrderItem(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.address
