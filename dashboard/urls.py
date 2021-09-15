from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('invoices/', invoiceList, name='invoices'),
    path('add-invoice/', addInvoice, name='add_invoice'),

    path('cart/', cartPage, name='cart'),
    path('products/', Products, name='products'),
    path('add-products', addProduct, name='add_product'),
    path('add-sales', addSales, name='add_sales'),
    path('sales', salesList, name='sales'),


    path('purchase/', purchaseList, name='purchase_list'),
    path('add_purchase/', addPurchase, name='add_purchase'),

    path('employees/', EmployeeList, name='employees'),
    path('employees/<str:name>/', employeeEarning, name='employee-history'),
    path('employees/<str:name>/previous-month/', employeePreviousEarning, name='employee-prev-history'),
    path('add-employee/', addEmployee, name='add_employee'),
    
    path('commissions-earned/', Payroll, name='salaries'),
    path('previous_month_salaries/', previousPayRoll,
         name='previous-salaries'),
    path('feruzi_previous-month-salaries_pdf',
         GeneratePDF.as_view(), name='feruzi-salary-pdf'),
    path('signup/', signup, name='signup'),
    path('overall-daily-report/', overallDailyReport,
         name='overall_daily_report'),
    path('overall_daily-report-pdf/', OverallDailyPDF.as_view(),
         name='overall_daily_report_pdf'),

    path('feruzi_daily-report', dailyReport, name='feruzi_daily_report'),
    path('feruzi_daily-report-pdf', DailyPDF.as_view(),
         name='feruzi_daily_report_pdf'),
    path('fourways-daily-report', dailyReport2, name='fourways_daily_report'),
    path('fourways-daily-report-pdf', DailyPDF2.as_view(),
         name='fourways_daily_report_pdf'),
    path('customers', CustomerList, name='customer_list'),
    path('customers/<str:name>/', CustomerHistory, name='customer-history'),
    path('customers-purchases/<str:name>/', CustomerSalesHistory, name='customer-purchases'),
    path('add-customers', addCustomer, name='add-customer'),

    path('monthly-overall-report', OverallMonthlyReport,
         name='monthly_overall_report'),
    path('monthly-overall-report-pdf', OVERALLMONPDF.as_view(),
         name='monthly_overall_report_pdf'),
    path('previous-month-overall-report-pdf', PreviousOVERALLPDF.as_view(),
         name='previous_month_overall_report_pdf'),

    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name="logout"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name='account/password_reset.html'),
         name='password_reset'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
