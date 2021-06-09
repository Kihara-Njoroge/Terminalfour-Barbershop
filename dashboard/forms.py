from django.db.models import fields
from django.forms import ModelForm
from django import forms
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
