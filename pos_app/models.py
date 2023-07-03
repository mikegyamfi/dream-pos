from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)
    domain = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    choices = (
        ("Sales Personnel", "Sales Personnel"),
        ("Admin", "Admin")
    )
    role = models.CharField(max_length=200, null=False, blank=False, choices=choices, default="Sales Personnel")
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    password1 = models.CharField(max_length=100, null=False, blank=False)
    password2 = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.first_name + "-" + self.username


class StoreInfo(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    domain = models.CharField(max_length=200, null=False, blank=False)
    code = models.PositiveIntegerField(null=False, blank=False)


class Category(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False, blank=False)
    domain = models.CharField(max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=True)
    status = models.BooleanField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    domain = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    # original_price = models.FloatField(null=True, blank=True, default=0.0)
    quantity_available = models.PositiveIntegerField(null=False, blank=False)
    choices = (
        ("S/S", "S/S"),
        ("Q/S", "Q/S"),
        ("M/S", "M/S"),
        ("A/S", "A/S"),
        ("B/S", "B/S"),
        ("E/L", "E/L")
    )
    size = models.CharField(max_length=200, choices=choices)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.size}"


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    domain = models.CharField(max_length=250, null=False, blank=False)
    product_qty = models.PositiveIntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()


class SoldItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sale_reference = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    customer_phone = models.CharField(max_length=50, null=True, blank=True, default=None)
    amount_paid = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    domain = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    total_price = models.FloatField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    closed_date = models.DateTimeField()

    def __str__(self):
        return str(self.product)


class DaysSale(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sale_reference = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    customer_phone = models.CharField(max_length=50, null=True, blank=True)
    amount_paid = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    choices = (
        ("Cash", "Cash"),
        ("Momo", "Momo"),
        ("Card", "Card")
    )
    payment_mode = models.CharField(max_length=100, null=False, blank=False, choices=choices, default="Cash")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    domain = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    total_price = models.FloatField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)


class IndividualDaySale(models.Model):
    day = models.DateField(default=datetime.today().date())
    domain = models.CharField(max_length=250, null=False, blank=False)
    total_sales = models.FloatField()
    checked = models.BooleanField(max_length=100, default=False)
    time_of_check = models.DateTimeField(auto_now_add=True)


class RestockHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    domain = models.CharField(max_length=200, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    restock_date = models.DateTimeField(auto_now_add=True)


class Timeline(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    domain = models.CharField(max_length=200, null=False, blank=False)
    activity = models.CharField(max_length=500, null=False, blank=False)
    time = models.DateTimeField(auto_now_add=True)