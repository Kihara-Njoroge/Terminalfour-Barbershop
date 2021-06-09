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

    path('previous-month-salaries_pdf', GeneratePDF.as_view(), name='salary-pdf'),

    path('daily-report', dailyReport, name='daily_report'),
    path('daily-report-pdf', DailyPDF.as_view(), name='daily_report_pdf'),
    path('fourways-daily-report', dailyReport2, name='fourways_daily_report'),
    path('fourways-daily-report-pdf', DailyPDF2.as_view(),
         name='fourways_daily_report_pdf'),
    path('overall-report', overall, name='overall_report'),
    path('overall-pdf', OVERALLPDF.as_view(), name='overall_pdf'),
]
