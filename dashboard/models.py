from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from phone_field import PhoneField


class Employee(models.Model):
    roles = (
        ('Barber', 'Barber'),
        ('Stylist', 'Stylist')
    )
    branch = (
        ('feruzi', 'feruzi',),
        ('fourways', 'fourways')
    )
    name = models.CharField(max_length=254, null=False, blank=False)
    role = models.CharField(max_length=254, choices=roles)
    email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number')
    id_number = models.IntegerField(unique=True)
    branch = models.CharField(max_length=254, choices=branch)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=254)
    price = models.IntegerField()

    def __str__(self):
        return self.name


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
    box_quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField(decimal_places=2, max_digits=10)
    VAT = models.DecimalField(decimal_places=2, max_digits=10)
    Total = models.DecimalField(decimal_places=2, max_digits=10)
    payment_method = models.CharField(max_length=254, choices=payment_choices)
    status = models.CharField(max_length=254, choices=status_options)
    branch = models.CharField(max_length=254, choices=branch)

    def __str__(self):
        return self.product


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
    service = models.ForeignKey(Service, on_delete=CASCADE)
    served_by = models.ForeignKey(Employee, on_delete=CASCADE)
    payment_method = models.CharField(max_length=254, choices=payment_choices)
    branch = models.CharField(max_length=254, choices=branch)
    Total = models.IntegerField()

    def __str__(self):
        return self.service
