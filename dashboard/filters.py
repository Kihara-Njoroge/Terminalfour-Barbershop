import django_filters
from django_filters import CharFilter, NumberFilter, DateFilter
from .models import *


class InvoiceFilter(django_filters.FilterSet):

    class Meta:
        model = Invoice
        fields = ['date_of_services', 'service', 'served_by']


class PurchaseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_of_purchase',
                            lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='date_of_purchase',
                          lookup_expr='lte', label='End Date')

    class Meta:
        model = Purchase
        fields = ['status']
