from django.db.models import fields
import django_filters
from django_filters import CharFilter, NumberFilter, DateFilter
from .models import *


class InvoiceFilter(django_filters.FilterSet):

    class Meta:
        model = Invoice
        fields = ['date_of_services', 'service', 'served_by']

class SalesFilter(django_filters.FilterSet):

    class Meta:
        model = Sale
        fields = ['product', 'date_of_sale', 'branch']


class PurchaseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_of_purchase',
                            lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='date_of_purchase',
                          lookup_expr='lte', label='End Date')

    class Meta:
        model = Purchase
        fields = ['status']


class CustomerFilter(django_filters.FilterSet):
    name = CharFilter(lookup_expr='icontains', label='Name')
    class Meta:
        model = Customer
        fields = ['birthday']
        

class CustomerHistoryFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_of_services', lookup_expr='gte', label='From Date')
    end_date = DateFilter(field_name='date_of_services', lookup_expr='lte', label='To Date')
    class Meta:
        model = Invoice
        fields = ['payment_method']

class CustomerSalesHistoryFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_of_services', lookup_expr='gte', label='From Date')
    end_date = DateFilter(field_name='date_of_services', lookup_expr='lte', label='To Date')
    class Meta:
        model = Sale
        fields = ['product', 'payment_method']

class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',
                      lookup_expr='icontains', label='Product')

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['description', 'price', 'image', 'vendor']

class EmployeeHistoryFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_of_services', lookup_expr='gte', label='From Date')
    end_date = DateFilter(field_name='date_of_services', lookup_expr='lte', label='To Date')
    class Meta:
        model = Invoice
        fields = ['served_by']