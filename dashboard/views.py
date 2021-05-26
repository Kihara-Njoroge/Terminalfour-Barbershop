from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from datetime import datetime, date, timedelta
from django.utils import timezone
from .models import *
from .forms import *
from .filters import *


# Create your views here.
def home(request):
    context = {}
    return render(request, 'home.html', context)


# Dashboard
def dashboard(request):
    current_month = datetime.now().month

    sales_today = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59)).count()
    sales_this_mon = Invoice.objects.filter(
        date_of_services__month=current_month)

    purchases_today = Purchase.objects.filter(date_of_purchase__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_purchase__lte=timezone.now().replace(hour=23, minute=59, second=59)).count()
    purchases_this_mon = Purchase.objects.filter(
        date_of_purchase__month=current_month)

    monthly_sales = sales_this_mon.count()
    monthly_purchases = purchases_this_mon.count()

    monthly_expenses = sum([i.Total for i in purchases_this_mon])
    monthly_income = sum([i.Total for i in sales_this_mon])

    data = [monthly_income, monthly_expenses]
    labels = ["Income", 'Expenses']

    # daily sales and purchases report
    sales = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))
    total_sales_today = sum([i.Total for i in sales])

    purchases = Purchase.objects.filter(date_of_purchase__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_purchase__lte=timezone.now().replace(hour=23, minute=59, second=59))
    total_purchases_today = sum([i.Total for i in purchases])

    cash = Invoice.objects.filter(payment_method='Cash', date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))
    cash_received = sum([i.Total for i in cash])

    mpesa = Invoice.objects.filter(payment_method='Mpesa', date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))
    mpesa_received = sum([i.Total for i in mpesa])

    bank = Invoice.objects.filter(payment_method='Bank', date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))
    bank_received = sum([i.Total for i in bank])

    context = {'sales_today': sales_today,
               'monthly_sales': monthly_sales,
               'purchases_today': purchases_today,
               'monthly_purchases': monthly_purchases,
               'total_sales_today': total_sales_today,
               'total_purchases_today': total_purchases_today,
               'cash_received': cash_received,
               'mpesa_received': mpesa_received,
               'bank_received': bank_received,
               'monthly_expenses': monthly_expenses,
               'monthly_income': monthly_income,
               'data': data,
               'labels': labels,
               }

    return render(request, 'index.html', context)


def invoiceList(request):
    invoices = Invoice.objects.all()
    myFilter = InvoiceFilter(request.GET, queryset=invoices)
    invoices = myFilter.qs
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {'invoices': invoices,
               'page_obj': page_obj, 'myFilter': myFilter}
    return render(request, 'invoice\invoices_list.html', context)


def addInvoice(request):
    form = InvoiceForm()
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoices')
    context = {'form': form}
    return render(request, 'invoice\invoice_add.html', context)


# Purschases
def purchaseList(request):
    purchases = Purchase.objects.all()
    myFilter = PurchaseFilter(request.GET, queryset=purchases)
    purchases = myFilter.qs
    paginator = Paginator(purchases, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {'purchases': purchases,
               'page_obj': page_obj, 'myFilter': myFilter}

    return render(request, 'purchases\purchases_list.html', context)


def addPurchase(request):
    form = PurchaseForm()
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')
    context = {'form': form}

    return render(request, 'purchases\purchase_add.html', context)


def employeeList(request):
    employee = Employee.objects.all()
    paginator = Paginator(employee, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {'employee': employee, 'page_obj': page_obj, }

    return render(request, 'employee/employees.html', context)


def addEmployee(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')
    context = {'form': form}

    return render(request, 'employee/add_employee.html', context)


def payRoll(request):
    current_mon = datetime.now().month
    employee = Employee.objects.all()
    paginator = Paginator(employee, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    current_month = datetime.now().strftime("%B")

    payroll = []

    for i in range(len(employee)):
        employee_name = employee[i]
        total_this_mon = Invoice.objects.filter(
            served_by=employee_name, date_of_services__month=current_mon)
        monthly_total = sum([i.Total for i in total_this_mon])
        role = employee[i].role
        customers_served = total_this_mon.count()
        if role == 'Stylist':
            commission = 0.5*monthly_total
        else:
            commission = 0.4*monthly_total

        payroll_dict = {'employee_name': employee_name, 'role': role,
                        'monthly_total': monthly_total, 'commision': commission,
                        'customers_served': customers_served
                        }
        payroll.append(payroll_dict)

        form = PayRollForm()
        if request.POST:
            form = PayRollForm(request.POST)
            if form.is_valid():
                form.employee = employee_name
                form.month = current_month
                form.customers_served = customers_served
                form.total = monthly_total
                form.commission = commission
                form.save()
            else:
                form = PayRollForm()

    context = {'employee_name': employee_name, 'page_obj': page_obj,
               'current_month': current_month,
               'monthly_total': monthly_total,
               'commission': commission,
               'customers_served': customers_served,
               'role': role,
               'payroll': payroll,
               'form': form

               }

    return render(request, 'employee/payroll.html', context)


def previousPayRoll(request):
    current_mon = datetime.now().month - 1
    employee = Employee.objects.all()
    paginator = Paginator(employee, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    previous_month = date.today().replace(day=1) - timedelta(1)
    previous_month.strftime("%B")

    payroll = []

    for i in range(len(employee)):
        employee_name = employee[i]
        total_prev_mon = Invoice.objects.filter(
            served_by=employee_name, date_of_services__month=current_mon)
        monthly_total = sum([i.Total for i in total_prev_mon])
        role = employee[i].role
        customers_served = total_prev_mon.count()
        if role == 'Stylist':
            commission = 0.5*monthly_total
        else:
            commission = 0.4*monthly_total

        payroll_dict = {'employee_name': employee_name, 'role': role,
                        'monthly_total': monthly_total, 'commision': commission,
                        'customers_served': customers_served
                        }
        payroll.append(payroll_dict)

    context = {'employee_name': employee_name, 'page_obj': page_obj,
               'previous_month': previous_month,
               'monthly_total': monthly_total,
               'commission': commission,
               'customers_served': customers_served,
               'role': role,
               'payroll': payroll,


               }

    return render(request, 'employee/previous_payroll.html', context)
