from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from datetime import datetime, date, timedelta
from django.utils import timezone
from .models import *
from .forms import *
from .filters import *
from .utils import *


# Create your views here.

# login


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Incorrect Username or Password!')
    context = {}
    return render(request, 'login_page.html', context)

# logout function


def logoutUser(request):
    logout(request)
    return redirect('login')

# Dashboard


@login_required(login_url='login')
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

    # monthly report
    feruzi_monthly_sale = sales_this_mon.filter(branch='feruzi')
    feruzi_monthly_sales = feruzi_monthly_sale.count()
    fourways_monthly_sale = sales_this_mon.filter(branch='fourways')
    fourways_monthly_sales = fourways_monthly_sale.count()
    monthly_sales = sales_this_mon.count()
    monthly_purchases = purchases_this_mon.count()

    fourways_monthly_total = sum([i.Total for i in fourways_monthly_sale])
    feruzi_monthly_total = sum([i.Total for i in feruzi_monthly_sale])

    monthly_mpesa = sales_this_mon.filter(payment_method='Mpesa')
    feruzi_mpesa_mon = monthly_mpesa.filter(branch='feruzi')
    feruzi_mpesa_received_mon = sum([i.Total for i in feruzi_mpesa_mon])
    fourways_mpesa_mon = monthly_mpesa.filter(branch='fourways')
    fourways_mpesa_received_mon = sum([i.Total for i in fourways_mpesa_mon])

    monthly_cash = sales_this_mon.filter(payment_method='Cash')
    feruzi_cash_mon = monthly_cash.filter(branch='feruzi')
    feruzi_cash_received_mon = sum([i.Total for i in feruzi_cash_mon])

    fourways_cash_mon = monthly_cash.filter(branch='fourways')
    fourways_cash_received_mon = sum([i.Total for i in fourways_cash_mon])

    monthly_bank = sales_this_mon.filter(payment_method='Bank')
    feruzi_bank_mon = monthly_bank.filter(branch='feruzi')
    feruzi_bank_received_mon = sum([i.Total for i in feruzi_bank_mon])

    fourways_bank_mon = monthly_mpesa.filter(branch='fourways')
    fourways_bank_received_mon = sum([i.Total for i in fourways_bank_mon])

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

    # branches report
    feruzi_todays_customers = sales.filter(branch='feruzi').count()

    feruzi_bank = bank.filter(branch='feruzi')
    feruzi_bank_received = sum([i.Total for i in feruzi_bank])
    feruzi_cash = cash.filter(branch='feruzi')
    feruzi_cash_received = sum([i.Total for i in feruzi_cash])
    feruzi_mpesa = mpesa.filter(branch='feruzi')
    feruzi_mpesa_received = sum([i.Total for i in feruzi_mpesa])
    feruzi_total = (feruzi_bank_received +
                    feruzi_cash_received+feruzi_mpesa_received)

    fourways_todays_customers = sales.filter(branch='fourways').count()
    fourways_bank = bank.filter(branch='fourways')
    fourways_bank_received = sum([i.Total for i in fourways_bank])
    fourways_cash = cash.filter(branch='fourways')
    fourways_cash_received = sum([i.Total for i in fourways_cash])
    fourways_mpesa = mpesa.filter(branch='fourways')
    fourways_mpesa_received = sum([i.Total for i in fourways_mpesa])
    fourways_total = (fourways_bank_received +
                      fourways_cash_received+fourways_mpesa_received)

    context = {'sales_today': sales_today,
               'monthly_sales': monthly_sales,
               'purchases_today': purchases_today,
               'monthly_purchases': monthly_purchases,
               'total_sales_today': total_sales_today,
               'total_purchases_today': total_purchases_today,
               'cash_received': cash_received,
               'mpesa_received': mpesa_received,
               'bank_received': bank_received,
               'fourways_mpesa_received': fourways_mpesa_received,
               'fourways_bank_received': fourways_bank_received,
               'fourways_cash_received': fourways_cash_received,
               'feruzi_mpesa_received': feruzi_mpesa_received,
               'feruzi_cash_received': feruzi_cash_received,
               'feruzi_bank_received': feruzi_bank_received,
               'fourways_mpesa_received_mon': fourways_mpesa_received_mon,
               'fourways_bank_received_mon': fourways_bank_received_mon,
               'fourways_cash_received_mon': fourways_cash_received_mon,
               'feruzi_mpesa_received_mon': feruzi_mpesa_received_mon,
               'feruzi_cash_received_mon': feruzi_cash_received_mon,
               'feruzi_bank_received_mon': feruzi_bank_received_mon,
               'fourways_todays_customers': fourways_todays_customers,
               'feruzi_todays_customers': feruzi_todays_customers,
               'fourways_total': fourways_total,
               'feruzi_total': feruzi_total,
               'fourways_monthly_sales': fourways_monthly_sales,
               'fourways_monthly_sales': fourways_monthly_sales,
               'feruzi_monthly_sales': feruzi_monthly_sales,
               'feruzi_monthly_total': feruzi_monthly_total,
               'fourways_monthly_total': fourways_monthly_total,



               }

    return render(request, 'index.html', context)


@login_required(login_url='login')
def invoiceList(request):
    invoice = Invoice.objects.all()
    myFilter = InvoiceFilter(request.GET, queryset=invoice)
    invoices = myFilter.qs
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'invoices': invoices,
               'page_obj': page_obj, 'myFilter': myFilter}
    return render(request, 'invoice\invoices_list.html', context)


@login_required(login_url='login')
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
@login_required(login_url='login')
def purchaseList(request):
    purchase = Purchase.objects.all()
    myFilter = PurchaseFilter(request.GET, queryset=purchase)
    purchases = myFilter.qs
    paginator = Paginator(purchases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'purchases': purchases,
               'page_obj': page_obj, 'myFilter': myFilter}

    return render(request, 'purchases\purchases_list.html', context)


@login_required(login_url='login')
def addPurchase(request):
    form = PurchaseForm()
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')
    context = {'form': form}

    return render(request, 'purchases\purchase_add.html', context)


@login_required(login_url='login')
def FeruziEmployeeList(request):
    employee = Employee.objects.all()
    employee = employee.filter(branch='feruzi')
    paginator = Paginator(employee, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'employee': employee, 'page_obj': page_obj, }

    return render(request, 'employee/feruzi_employees.html', context)


@login_required(login_url='login')
def FourwaysEmployeeList(request):
    employee = Employee.objects.all()
    employee = employee.filter(branch='fourways')
    paginator = Paginator(employee, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'employee': employee, 'page_obj': page_obj, }

    return render(request, 'employee/fourways_employees.html', context)


@login_required(login_url='login')
def addEmployee(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')
    context = {'form': form}

    return render(request, 'employee/add_employee.html', context)


@login_required(login_url='login')
def FeruzipayRoll(request):
    current_mon = datetime.now().month
    worker = Employee.objects.all()
    employee = worker.filter(branch='feruzi')
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

        branch = employee[i].branch

        payroll_dict = {'employee_name': employee_name, 'role': role,
                        'monthly_total': monthly_total, 'commision': commission,
                        'customers_served': customers_served, 'branch': branch,
                        }
        payroll.append(payroll_dict)

    context = {'employee_name': employee_name, 'page_obj': page_obj,
               'current_month': current_month,
               'monthly_total': monthly_total,
               'commission': commission,
               'customers_served': customers_served,
               'role': role,
               'payroll': payroll,

               }

    return render(request, 'employee/feruzi_payroll.html', context)


@login_required(login_url='login')
def FourwayspayRoll(request):
    current_mon = datetime.now().month
    worker = Employee.objects.all()
    employee = worker.filter(branch='fourways')
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

        branch = employee[i].branch

        payroll_dict = {'employee_name': employee_name, 'role': role,
                        'monthly_total': monthly_total, 'commision': commission,
                        'customers_served': customers_served, 'branch': branch,
                        }
        payroll.append(payroll_dict)

    context = {'employee_name': employee_name, 'page_obj': page_obj,
               'current_month': current_month,
               'monthly_total': monthly_total,
               'commission': commission,
               'customers_served': customers_served,
               'role': role,
               'payroll': payroll,

               }

    return render(request, 'employee/fourways_payroll.html', context)


@login_required(login_url='login')
def FeruzipreviousPayRoll(request):
    current_mon = datetime.now().month - 1
    worker = Employee.objects.all()
    employee = worker.filter(branch='feruzi')
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

    return render(request, 'employee/feruzi_previous_payroll.html', context)


@method_decorator(login_required, name='dispatch')
class FeruziGeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('employee/feruzi_previous_payroll_pdf.html')
        current_mon = datetime.now().month - 1
        worker = Employee.objects.all()
        employee = worker.filter(branch='feruzi')
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
        html = template.render(context)
        name = "TerminalfourCommissions(str(previous_month))"
        pdf = render_to_pdf(
            'employee/feruzi_previous_payroll_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Terminalfour_Commissions_%s.pdf" % (
                "12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required(login_url='login')
def FourwayspreviousPayRoll(request):
    current_mon = datetime.now().month - 1
    worker = Employee.objects.all()
    employee = worker.filter(branch='fourways')
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

    return render(request, 'employee/fourways_previous_payroll.html', context)


@method_decorator(login_required, name='dispatch')
class FourwaysGeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('employee/fourways_previous_payroll_pdf.html')
        current_mon = datetime.now().month - 1
        worker = Employee.objects.all()
        employee = worker.filter(branch='fourways')
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
        html = template.render(context)
        pdf = render_to_pdf(
            'employee/fourways_previous_payroll_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Fourways_Commissions_%s.pdf" % (
                "12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required(login_url='login')
def overallDailyReport(request):
    feruzi = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))

    total_customers = feruzi.count()

    shave = feruzi.filter(service=1)
    spa = feruzi.filter(service=2)
    styling = feruzi.filter(service=3)

    shave_count = shave.count()
    spa_count = spa.count()
    styling_count = styling.count()

    shave_total = sum([i.Total for i in shave])
    spa_total = sum([i.Total for i in spa])
    styling_total = sum([i.Total for i in styling])

    feruzi_totals = (shave_total+styling_total+spa_total)

    context = {'total_customers': total_customers,
               'shave_count': shave_count,
               'spa_count': spa_count,
               'styling_count': styling_count,
               'spa_total': spa_total,
               'shave_total': shave_total,
               'styling_total': styling_total,
               'feruzi_totals': feruzi_totals
               }
    return render(request, 'reports/overall_daily_report.html', context)


@method_decorator(login_required, name='dispatch')
class OverallDailyPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/overall_daily_report_pdf.html')
        today = str(date.today())

        sales = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
            hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))

        total_customers = sales.count()

        shave = sales.filter(service=1)
        spa = sales.filter(service=2)
        styling = sales.filter(service=3)

        shave_count = shave.count()
        spa_count = spa.count()
        styling_count = styling.count()

        shave_total = sum([i.Total for i in shave])
        spa_total = sum([i.Total for i in spa])
        styling_total = sum([i.Total for i in styling])

        totals = (shave_total+styling_total+spa_total)

        context = {
            'today': today,
            'total_customers': total_customers,
            'shave_count': shave_count,
            'spa_count': spa_count,
            'styling_count': styling_count,
            'spa_total': spa_total,
            'shave_total': shave_total,
            'styling_total': styling_total,
            'totals': totals
        }

        html = template.render(context)

        pdf = render_to_pdf('reports/overall_daily_report_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Overall_Daily_Report%s.pdf" % (
                "12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

# Feruzi daily Report


@login_required(login_url='login')
def dailyReport(request):
    sales = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))
    feruzi = sales.filter(branch='feruzi')
    total_customers = feruzi.count()

    shave = feruzi.filter(service=1)
    spa = feruzi.filter(service=2)
    styling = feruzi.filter(service=3)

    shave_count = shave.count()
    spa_count = spa.count()
    styling_count = styling.count()

    shave_total = sum([i.Total for i in shave])
    spa_total = sum([i.Total for i in spa])
    styling_total = sum([i.Total for i in styling])

    feruzi_totals = (shave_total+styling_total+spa_total)

    context = {'total_customers': total_customers,
               'shave_count': shave_count,
               'spa_count': spa_count,
               'styling_count': styling_count,
               'spa_total': spa_total,
               'shave_total': shave_total,
               'styling_total': styling_total,
               'feruzi_totals': feruzi_totals
               }
    return render(request, 'reports/feruzi_daily_report.html', context)


@method_decorator(login_required, name='dispatch')
class DailyPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/feruzi_daily_report_pdf.html')
        today = str(date.today())

        sales = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
            hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))
        feruzi = sales.filter(branch='feruzi')
        total_customers = feruzi.count()

        shave = feruzi.filter(service=1)
        spa = feruzi.filter(service=2)
        styling = feruzi.filter(service=3)

        shave_count = shave.count()
        spa_count = spa.count()
        styling_count = styling.count()

        shave_total = sum([i.Total for i in shave])
        spa_total = sum([i.Total for i in spa])
        styling_total = sum([i.Total for i in styling])

        feruzi_totals = (shave_total+styling_total+spa_total)

        context = {
            'today': today,
            'total_customers': total_customers,
            'shave_count': shave_count,
            'spa_count': spa_count,
            'styling_count': styling_count,
            'spa_total': spa_total,
            'shave_total': shave_total,
            'styling_total': styling_total,
            'feruzi_totals': feruzi_totals
        }

        html = template.render(context)

        pdf = render_to_pdf('reports/feruzi_daily_report_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Daily_Report_Feruzi%s.pdf" % (
                "12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


# Fourways Daily Report
@login_required(login_url='login')
def dailyReport2(request):
    sales = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))
    fourways = sales.filter(branch='fourways')
    total_customers = fourways.count()

    shave = fourways.filter(service=1)
    spa = fourways.filter(service=2)
    styling = fourways.filter(service=3)

    shave_count = shave.count()
    spa_count = spa.count()
    styling_count = styling.count()

    shave_total = sum([i.Total for i in shave])
    spa_total = sum([i.Total for i in spa])
    styling_total = sum([i.Total for i in styling])

    fourways_totals = (shave_total+styling_total+spa_total)

    context = {'total_customers': total_customers,
               'shave_count': shave_count,
               'spa_count': spa_count,
               'styling_count': styling_count,
               'spa_total': spa_total,
               'shave_total': shave_total,
               'styling_total': styling_total,
               'fourways_totals': fourways_totals
               }
    return render(request, 'reports/fourways_daily_report.html', context)


@method_decorator(login_required, name='dispatch')
class DailyPDF2(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/fourways_daily_report_pdf.html')
        today = str(date.today())

        sales = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
            hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))
        fourways = sales.filter(branch='fourways')
        total_customers = fourways.count()

        shave = fourways.filter(service=1)
        spa = fourways.filter(service=2)
        styling = fourways.filter(service=3)

        shave_count = shave.count()
        spa_count = spa.count()
        styling_count = styling.count()

        shave_total = sum([i.Total for i in shave])
        spa_total = sum([i.Total for i in spa])
        styling_total = sum([i.Total for i in styling])

        fourways_totals = (shave_total+styling_total+spa_total)

        context = {
            'today': today,
            'total_customers': total_customers,
            'shave_count': shave_count,
            'spa_count': spa_count,
            'styling_count': styling_count,
            'spa_total': spa_total,
            'shave_total': shave_total,
            'styling_total': styling_total,
            'fourways_totals': fourways_totals
        }

        html = template.render(context)

        pdf = render_to_pdf('reports/fourways_daily_report_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Daily_Report_Feruzi%s.pdf" % (
                "12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

# Overall Daily Report


@login_required(login_url='login')
def overall(request):
    sales = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))

    daily_customers = sales.count()
    overall_total = sum([i.Total for i in sales])
    shave = sales.filter(service=1)
    shave_count = shave.count()
    shave_total = sum([i.Total for i in shave])

    spa = sales.filter(service=2)
    spa_count = spa.count()
    spa_total = sum([i.Total for i in shave])

    styling = sales.filter(service=3)
    styling_count = styling.count()
    styling_total = sum([i.Total for i in styling])

    context = {
        'styling_count': styling_count,
        'styling_total': styling_total,
        'shave_count': shave_count,
        'shave_total': shave_total,
        'spa_count': spa_count,
        'spa_total': spa_total,
        'daily_customers': daily_customers,
        'overall_total': overall_total
    }
    return render(request, 'reports/overall_report.html', context)


@method_decorator(login_required, name='dispatch')
class OVERALLPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/overall_report_pdf.html')
        today = str(date.today())

        sales = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
            hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59))

        daily_customers = sales.count()
        overall_total = sum([i.Total for i in sales])
        shave = sales.filter(service=1)
        shave_count = shave.count()
        shave_total = sum([i.Total for i in shave])

        spa = sales.filter(service=2)
        spa_count = spa.count()
        spa_total = sum([i.Total for i in spa])

        styling = sales.filter(service=3)
        styling_count = styling.count()
        styling_total = sum([i.Total for i in styling])

        overall_total = (shave_total+styling_total+spa_total)

        context = {
            'today': today,
            'styling_count': styling_count,
            'styling_total': styling_total,
            'shave_count': shave_count,
            'shave_total': shave_total,
            'spa_count': spa_count,
            'spa_total': spa_total,
            'daily_customers': daily_customers,
            'overall_total': overall_total
        }

        html = template.render(context)

        pdf = render_to_pdf('reports/overall_report_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Overall_Daily_Report%s.pdf" % (
                "12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


# monthly Reports
@login_required(login_url='login')
def OverallMonthlyReport(request):
    current_month = datetime.now().month
    sales = Invoice.objects.filter(date_of_services__month=current_month)
    current_mon = datetime.now().strftime("%B")
    total_customers = sales.count()

    shaving = sales.filter(service=1)
    shaving_count = shaving.count()
    shaving_total = sum([i.Total for i in shaving])

    spa = sales.filter(service=2)
    spa_count = spa.count()
    spa_total = sum([i.Total for i in spa])

    styling = sales.filter(service=3)
    styling_count = styling.count()
    styling_total = sum([i.Total for i in styling])

    overall_totals = sum([i.Total for i in sales])

    context = {
        'shaving_total': shaving_total,
        'shaving_count': shaving_count,
        'spa_count': spa_count,
        'spa_total': spa_total,
        'styling_count': styling_count,
        'styling_total': styling_total,
        'total_customers': total_customers,
        'overall_totals': overall_totals,
        'current_mon': current_mon,


    }

    return render(request, 'reports/overall_monthly_report.html', context)


@method_decorator(login_required, name='dispatch')
class OVERALLMONPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/overall_monthly_report_pdf.html')
        current_month = datetime.now().month
        today = str(date.today())
        sales = Invoice.objects.filter(date_of_services__month=current_month)

        total_customers = sales.count()

        shaving = sales.filter(service=1)
        shaving_count = shaving.count()
        shaving_total = sum([i.Total for i in shaving])

        spa = sales.filter(service=2)
        spa_count = spa.count()
        spa_total = sum([i.Total for i in spa])

        styling = sales.filter(service=3)
        styling_count = styling.count()
        styling_total = sum([i.Total for i in styling])

        overall_totals = sum([i.Total for i in sales])

        context = {
            'shaving_total': shaving_total,
            'shaving_count': shaving_count,
            'spa_count': spa_count,
            'spa_total': spa_total,
            'styling_count': styling_count,
            'styling_total': styling_total,
            'total_customers': total_customers,
            'overall_totals': overall_totals,
            'current_month ': current_month,
            'today': today,


        }

        html = template.render(context)

        pdf = render_to_pdf('reports/overall_monthly_report_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Overall_Monthly_Report%s.pdf" % (
                "12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@method_decorator(login_required, name='dispatch')
class PreviousOVERALLPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/previou_mon_overall_report.html')
        current_month = datetime.now().month - 1
        previous_month = date.today().replace(day=1) - timedelta(1)
        previous_month.strftime("%B")
        today = str(date.today())
        sales = Invoice.objects.filter(date_of_services__month=current_month)

        total_customers = sales.count()

        shaving = sales.filter(service=1)
        shaving_count = shaving.count()
        shaving_total = sum([i.Total for i in shaving])

        spa = sales.filter(service=2)
        spa_count = spa.count()
        spa_total = sum([i.Total for i in spa])

        styling = sales.filter(service=3)
        styling_count = styling.count()
        styling_total = sum([i.Total for i in styling])

        overall_totals = sum([i.Total for i in sales])

        context = {
            'shaving_total': shaving_total,
            'shaving_count': shaving_count,
            'spa_count': spa_count,
            'spa_total': spa_total,
            'styling_count': styling_count,
            'styling_total': styling_total,
            'total_customers': total_customers,
            'overall_totals': overall_totals,
            'current_month ': current_month,
            'today': today,
            'previous_month': previous_month


        }

        html = template.render(context)

        pdf = render_to_pdf('reports/previou_mon_overall_report.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Previous_Month_Overall_Report%s.pdf" % (
                "12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
