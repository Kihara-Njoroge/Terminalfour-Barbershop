from django.db.models import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import ModelSignal
from django.forms import ModelForm
from .models import *


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ['invoice_no', 'invoice_id']


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        exclude = ['purchase_no', 'purchase_id']


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

# branches

class SignUpForm(UserCreationForm):


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class SalesForm(ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"