from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),

    path('invoices/', invoiceList, name='invoices'),
    path('add-invoice/', addInvoice, name='add_invoice'),

    path('purchase/', purchaseList, name='purchase_list'),
    path('add_purchase/', addPurchase, name='add_purchase'),

    path('employees/', employeeList, name='employees'),
    path('add-employee/', addEmployee, name='add_employee'),
    path('salaries/', payRoll, name='salaries'),
    path('previous-month-salaries', previousPayRoll, name='previous_payroll'),

    path('previous-month-salaries_pdf', GeneratePDF.as_view(), name='salary-pdf')
]
