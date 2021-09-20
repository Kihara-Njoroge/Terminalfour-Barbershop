from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.deletion import CASCADE
from phone_field import PhoneField
import math

class Customer(models.Model):
    name = models.CharField(max_length=254)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    birthday = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    branch = (
        ('feruzi', 'feruzi',),
        ('fourways', 'fourways')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=254, choices=branch)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Employee(models.Model):
    name = models.CharField(max_length=254, null=False, blank=False)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    id_number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.name)


class Service(models.Model):
    name = models.CharField(max_length=254)
    percentage = models.IntegerField()


    def __str__(self):
        return str(self.name)


class Purchase(models.Model):
    payment_choices = (
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
        ('Mpesa', 'Mpesa'),
    )
    status_options = (
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
    )
    branch = (
        ('feruzi', 'feruzi',),
        ('fourways', 'fourways')
    )
    date_of_purchase = models.DateTimeField(auto_now_add=True, null=True)
    purchase_no = models.AutoField(primary_key=True)
    purchase_id = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.CharField(max_length=254)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField(decimal_places=2, max_digits=10)
    VAT = models.DecimalField(decimal_places=2, max_digits=10)
    Total = models.DecimalField(decimal_places=2, max_digits=10)
    payment_method = models.CharField(max_length=254, choices=payment_choices)
    status = models.CharField(max_length=254, choices=status_options)
    branch = models.CharField(max_length=254, choices=branch)

    def __str__(self):
        return str(self.product)


class Invoice(models.Model):
    payment_choices = (
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
        ('Mpesa', 'Mpesa'),
    )
    branch = (
        ('feruzi', 'feruzi',),
        ('fourways', 'fourways')
    )
    invoice_no = models.AutoField(primary_key=True)
    invoice_id = models.UUIDField(default=uuid.uuid4, editable=False)
    date_of_services = models.DateTimeField(auto_now_add=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    service = models.ForeignKey(Service, on_delete=CASCADE)
    served_by = models.ForeignKey(Employee, on_delete=CASCADE)
    payment_method = models.CharField(max_length=254, choices=payment_choices)
    branch = models.CharField(
        max_length=254, choices=branch, default='fourways')
    Total = models.IntegerField()

    def __str__(self):
        return str(self.service)
    @property
    def get_total(self):
        total = self.Total
        return total
    @property
    def get_percentage(self):
        percentage = self.service.percentage
        return percentage

    @property
    def get_commission(self):
        percentage = self.service.percentage
        commission = self.Total * (percentage/100)
        return commission


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Sale(models.Model):
    payment_choices = (
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
        ('Mpesa', 'Mpesa'),
    )
    branch = (
        ('feruzi', 'feruzi',),
        ('fourways', 'fourways')
    )
    sales_no = models.AutoField(primary_key=True)
    sales_id = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=20, choices=payment_choices)
    branch = models.CharField(max_length=20, choices=branch)
    date_of_sale = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sales_id)
