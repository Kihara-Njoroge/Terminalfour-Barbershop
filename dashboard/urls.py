from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),

    path('invoices/', invoiceList, name='invoices'),
    path('add-invoice/', addInvoice, name='add_invoice'),

    path('purchase/', purchaseList, name='purchase_list'),
    path('add_purchase/', addPurchase, name='add_purchase'),

    path('feruzi_employees/', FeruziEmployeeList, name='feruzi_employees'),
    path('fourways_employees/', FourwaysEmployeeList, name='fourways_employees'),
    path('add-employee/', addEmployee, name='add_employee'),
    path('feruzi_salaries/', FeruzipayRoll, name='feruzi-salaries'),
    path('fourways_salaries/', FourwayspayRoll, name='fourways-salaries'),
    path('feruzi_previous_salaries/', FeruzipreviousPayRoll,
         name='feruzi-previous-salaries'),
    path('feruzi_previous-month-salaries_pdf',
         FeruziGeneratePDF.as_view(), name='feruzi-salary-pdf'),
    path('fourways_previous_salaries/', FourwayspreviousPayRoll,
         name='fourways-previous-salaries'),
    path('fourways_previous-month-salaries_pdf',
         FourwaysGeneratePDF.as_view(), name='fourways-salary-pdf'),


    path('overall-daily-report', overallDailyReport, name='overall_daily_report'),
    path('overall_daily-report-pdf', OverallDailyPDF.as_view(),
         name='overall_daily_report_pdf'),

    path('feruzi_daily-report', dailyReport, name='feruzi_daily_report'),
    path('feruzi_daily-report-pdf', DailyPDF.as_view(),
         name='feruzi_daily_report_pdf'),
    path('fourways-daily-report', dailyReport2, name='fourways_daily_report'),
    path('fourways-daily-report-pdf', DailyPDF2.as_view(),
         name='fourways_daily_report_pdf'),
    path('overall-report', overall, name='overall_report'),
    path('overall-pdf', OVERALLPDF.as_view(), name='overall_pdf'),


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
