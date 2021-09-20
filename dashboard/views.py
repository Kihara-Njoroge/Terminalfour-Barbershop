from django.core import paginator
from django.db.models import query
from django.forms.utils import pretty_name
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls.conf import path
from django.views.generic import View
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib import messages
from django.utils.decorators import method_decorator
from datetime import datetime, date, timedelta
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from .models import *
from .forms import *
from .filters import *
from .utils import *


# Create your views here.
@unauthenticated_user
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# login
@unauthenticated_user
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

# logout
def logoutUser(request):
    logout(request)
    return redirect('login')

# Dashboard
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
    prod_sales = Sale.objects.filter(date_of_sale__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_sale__lte=timezone.now().replace(hour=23, minute=59, second=59))
    prod_sales_mon = Sale.objects.filter(date_of_sale__month=current_month)
    #daily sales
    feruzi_prod = prod_sales.filter(branch='feruzi')
    feruzi_prod_sales = sum([i.amount for i in feruzi_prod])
    fourways_prod = prod_sales.filter(branch='fourways')
    fourways_prod_sales = sum([i.amount for i in fourways_prod])

    #monthly sales
    feruzi_prod_mon = prod_sales_mon.filter(branch='feruzi')
    feruzi_prod_mon_sales = sum([i.amount for i in feruzi_prod_mon])
    fourways_prod_mon = prod_sales_mon.filter(branch='fourways')
    fourways_prod_mon_sales = sum([i.amount for i in fourways_prod_mon])


        

    # monthly report

    feruzi_monthly_sale = sales_this_mon.filter(branch='feruzi')
    feruzi_monthly_sales = feruzi_monthly_sale.count()
    fourways_monthly_sale = sales_this_mon.filter(branch='fourways')
    fourways_monthly_sales = fourways_monthly_sale.count()
    monthly_sales = sales_this_mon.count()
    monthly_purchases = purchases_this_mon.count()

    fourways_monthly_total = sum([i.Total for i in fourways_monthly_sale], fourways_prod_mon_sales)
    feruzi_monthly_total = sum([i.Total for i in feruzi_monthly_sale], feruzi_prod_mon_sales)

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
                    feruzi_cash_received+feruzi_mpesa_received+feruzi_prod_sales)

    fourways_todays_customers = sales.filter(branch='fourways').count()
    fourways_bank = bank.filter(branch='fourways')
    fourways_bank_received = sum([i.Total for i in fourways_bank])
    fourways_cash = cash.filter(branch='fourways')
    fourways_cash_received = sum([i.Total for i in fourways_cash])
    fourways_mpesa = mpesa.filter(branch='fourways')
    fourways_mpesa_received = sum([i.Total for i in fourways_mpesa])
    fourways_total = (fourways_bank_received +
                      fourways_cash_received+fourways_mpesa_received+fourways_prod_sales)

    total_income = sum([feruzi_total, fourways_total])
    total_income_mon = feruzi_monthly_total+fourways_monthly_total

    context = {'sales_today': sales_today,
                'feruzi_prod_sales':feruzi_prod_sales,
                'feruzi_prod_mon_sales':feruzi_prod_mon_sales,
                'fourways_prod_mon_sales':fourways_prod_mon_sales,
                'fourways_prod_sales':fourways_prod_sales,
                'total_income':total_income,
                'total_income_mon':total_income_mon,
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
#Invoices
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def invoiceList(request):
    invoice = Invoice.objects.all().order_by('-date_of_services')
    myFilter = InvoiceFilter(request.GET, queryset=invoice)
    invoices = myFilter.qs
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'invoices': invoices,
               'page_obj': page_obj, 'myFilter': myFilter}
    return render(request, 'invoice/invoices_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addInvoice(request):
    form = InvoiceForm()
    customers = Customer.objects.all()
    myFilter = CustomerFilter(request.GET, queryset=customers)
    if request.method == 'GET':
        user = get_user(request)
        branch = user.profile.branch
        form = InvoiceForm()

    if request.method == 'POST':
        user = get_user(request)
        branch = user.profile.branch
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoices')
    context = {'form': form, 'myFilter': myFilter, 'branch': branch}
    return render(request, 'invoice/invoice_add.html', context)


# Purschases
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def purchaseList(request):
    purchase = Purchase.objects.all().order_by('-date_of_purchase')
    myFilter = PurchaseFilter(request.GET, queryset=purchase)
    purchases = myFilter.qs
    paginator = Paginator(purchases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'purchases': purchases,
               'page_obj': page_obj, 'myFilter': myFilter}

    return render(request, 'purchases/purchases_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addPurchase(request):
    form = PurchaseForm()
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')
    context = {'form': form}
    return render(request, 'purchases/purchase_add.html', context)


#Employees
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def EmployeeList(request):
    employee = Employee.objects.all().order_by('name')
    paginator = Paginator(employee, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'employee': employee, 'page_obj': page_obj, }

    return render(request, 'employee/employees.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employeeEarning(request, name):
    current_month = datetime.now().month
    employee = Employee.objects.get(name=name)
    invoice = Invoice.objects.filter(date_of_services__month=current_month, served_by=employee).order_by('-date_of_services')
    myFilter = InvoiceFilter(request.GET, queryset=invoice)
    invoice = myFilter.qs
    paginator = Paginator(invoice, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    this_month = date.today()
    this_month.strftime("%B")

    total = 0
    for item in page_obj:
        total += item.get_commission

    

    context = {'invoice': invoice, 'employee':employee, 'total':total,'this_month':this_month,
               'page_obj': page_obj, 'myFilter': myFilter}
    return render(request, 'employee/employee_history.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def employeePreviousEarning(request, name):
    current_month = datetime.now().month - 1
    employee = Employee.objects.get(name=name)
    invoice = Invoice.objects.filter(date_of_services__month=current_month, served_by=employee).order_by('-date_of_services')
    myFilter = InvoiceFilter(request.GET, queryset=invoice)
    invoice = myFilter.qs
    paginator = Paginator(invoice, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    previous_month = date.today().replace(day=1) - timedelta(1)
    previous_month.strftime("%B")


    total = 0
    for item in page_obj:
        total += item.get_commission

    

    context = {'invoice': invoice, 'employee':employee, 'total':total,'previous_month':previous_month,
               'page_obj': page_obj, 'myFilter': myFilter}
    return render(request, 'employee/employee-previous-mon.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addEmployee(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')
    context = {'form': form}

    return render(request, 'employee/add_employee.html', context)


#Payrolls
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Payroll(request):
    current_month = datetime.now().month
    employee = Employee.objects.all()
    this_month = date.today()
    this_month.strftime("%B")
    paginator = Paginator(employee, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    payroll = []
    for i in range(len(employee)):
        name = employee[i]
        total_prev_mon = Invoice.objects.filter(
                served_by=name, date_of_services__month=current_month)
        clients = total_prev_mon.count()
        total_earned = sum([i.Total for i in total_prev_mon])
        total_commission =  sum([i.get_commission for i in total_prev_mon])
        payroll_dict = { 'name':name, 'total_commission':total_commission,'total_earned':total_earned, 'clients':clients, 'this_month':this_month}
        payroll.append(payroll_dict)
        print(payroll)


        context = {'payroll':payroll, 'this_month':this_month, 'page_obj':page_obj}

    return render(request, 'employee/current-mon-payroll.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def previousPayRoll(request):
    current_month = datetime.now().month - 1
    employee = Employee.objects.all()
    previous_month = date.today().replace(day=1) - timedelta(1)
    previous_month.strftime("%B")
    paginator = Paginator(employee, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    payroll = []
    for i in range(len(employee)):
        name = employee[i]
        total_prev_mon = Invoice.objects.filter(
                served_by=name, date_of_services__month=current_month)
        clients = total_prev_mon.count()
        total_earned = sum([i.Total for i in total_prev_mon])
        total_commission =  sum([i.get_commission for i in total_prev_mon])
        payroll_dict = { 'name':name, 'total_commission':total_commission,'total_earned':total_earned, 'clients':clients, 'previous_month':previous_month}
        payroll.append(payroll_dict)
        print(payroll)


        context = {'payroll':payroll, 'previous_month':previous_month, 'page_obj':page_obj}

    return render(request, 'employee/previous_payroll.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('employee/previous_payroll_pdf.html')
        current_month = datetime.now().month - 1
        employee = Employee.objects.all()
        previous_month = date.today().replace(day=1) - timedelta(1)
        previous_month.strftime("%B")
        payroll = []
        print(employee)
        
        for i in range(len(employee)):
            name = employee[i]
            total_prev_mon = Invoice.objects.filter(
                served_by=name, date_of_services__month=current_month)
            clients = total_prev_mon.count()
            total_earned = sum([i.Total for i in total_prev_mon])
            total_commission =  sum([i.get_commission for i in total_prev_mon])
            payroll_dict = { 'name':name, 'total_commission':total_commission,'total_earned':total_earned, 'clients':clients, 'previous_month':previous_month}
            payroll.append(payroll_dict)
            print(payroll)


        context = {'payroll':payroll, 'previous_month':previous_month}
        pdf = render_to_pdf(
            'employee/previous_payroll_pdf.html', context)
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

#Daily Reports

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def overallDailyReport(request):
    services = Service.objects.all()
    sales = Sale.objects.filter(date_of_sale__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_sale__lte=timezone.now().replace(hour=23, minute=59, second=59))
    sales_amount = sum([i.amount for i in sales])
    sales_count = sales.count()
    services_list = []
    services_dict = {}
    total_customers = 0
    total_income = 0




    for service in services:
        name = service.name
        id = service.id
        invoice = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59), service=id)
        

        total_count =  invoice.count()
        total_amount = sum([i.Total for i in invoice])

        total_customers += total_count
        total_income += total_amount

        services_dict = {'name':name, 'total_count':total_count, 'total_amount':total_amount}

        services_list.append(services_dict)

        context = {'services_list':services_list, 'total_customers':total_customers,'total_income':total_income,
                    'sales_amount':sales_amount, 'sales_count':sales_count}

        

    return render(request, 'reports/overall_daily_report.html', context)



@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class OverallDailyPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/overall_daily_report_pdf.html')
        today = str(date.today())
        services = Service.objects.all()
        sales = Sale.objects.filter(date_of_sale__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_sale__lte=timezone.now().replace(hour=23, minute=59, second=59))
        sales_amount = sum([i.amount for i in sales])
        sales_count = sales.count()
        services_list = []
        services_dict = {}
        total_customers = 0
        total_income = 0
        for service in services:
            name = service.name
            id = service.id
   
            invoice = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
            hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59), service=id)
            total_count =  invoice.count()
            total_amount = sum([i.Total for i in invoice])
            total_customers += total_count
            total_income += total_amount
            services_dict = {'name':name, 'total_count':total_count, 'total_amount':total_amount}

            services_list.append(services_dict)
            print(services_list)

            context = {'services_list':services_list, 'total_customers':total_customers,'total_income':total_income,
                        'sales_count':sales_count,'sales_amount':sales_amount}


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
@allowed_users(allowed_roles=['admin'])
def dailyReport(request):
    services = Service.objects.all()
    sales = Sale.objects.filter(date_of_sale__gte=timezone.now().replace(
    hour=0, minute=0, second=0), date_of_sale__lte=timezone.now().replace(hour=23, minute=59, second=59),branch='feruzi')
    sales_amount = sum([i.amount for i in sales])
    sales_count = sales.count()
    services_list = []
    services_dict = {}
    total_customers = 0
    total_income = 0
    for service in services:
        name = service.name
        id = service.id
        invoice = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59),branch='feruzi',service=id)
        total_count =  invoice.count()
        total_amount = sum([i.Total for i in invoice])
        total_customers += total_count
        total_income += total_amount
        services_dict = {'name':name, 'total_count':total_count, 'total_amount':total_amount}

        services_list.append(services_dict)

    context = {'services_list':services_list, 'total_customers':total_customers,'total_income':total_income,
                        'sales_amount':sales_amount,'sales_count':sales_count,}

    return render(request, 'reports/feruzi_daily_report.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class DailyPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/feruzi_daily_report_pdf.html')
        services = Service.objects.all()
        sales = Sale.objects.filter(date_of_sale__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_sale__lte=timezone.now().replace(hour=23, minute=59, second=59),branch='feruzi')
        sales_amount = sum([i.amount for i in sales])
        sales_count = sales.count()
        services_list = []
        services_dict = {}
        total_customers = 0
        total_income = 0
        for service in services:
            name = service.name
            id = service.id
            invoice = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
            hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59),branch='feruzi',service=id)
            total_count =  invoice.count()
            total_amount = sum([i.Total for i in invoice])
            total_customers += total_count
            total_income += total_amount
            services_dict = {'name':name, 'total_count':total_count, 'total_amount':total_amount}

            services_list.append(services_dict)

            context = {'services_list':services_list, 'total_customers':total_customers,'total_income':total_income,
                        'sales_amount':sales_amount,'sales_count':sales_count,}

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
@allowed_users(allowed_roles=['admin'])
def dailyReport2(request):
    services = Service.objects.all()
    sales = Sale.objects.filter(date_of_sale__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_sale__lte=timezone.now().replace(hour=23, minute=59, second=59),branch='fourways')
    sales_amount = sum([i.amount for i in sales])
    sales_count = sales.count()
    services_list = []
    services_dict = {}
    total_customers = 0
    total_income = 0
    for service in services:
        name = service.name
        id = service.id
        invoice = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59),branch='fourways',service=id)
        total_count =  invoice.count()
        total_amount = sum([i.Total for i in invoice])
        total_customers += total_count
        total_income += total_amount
        services_dict = {'name':name, 'total_count':total_count, 'total_amount':total_amount}
        services_list.append(services_dict)

    context = {'services_list':services_list, 'total_customers':total_customers,'total_income':total_income,
                'sales_amount':sales_amount,'sales_count':sales_count,}
    return render(request, 'reports/fourways_daily_report.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class DailyPDF2(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/fourways_daily_report_pdf.html')
        today = str(date.today())
        sales = Sale.objects.filter(date_of_sale__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_of_sale__lte=timezone.now().replace(hour=23, minute=59, second=59),branch='fourways')
        sales_amount = sum([i.amount for i in sales])
        sales_count = sales.count()
            
        services = Service.objects.all()
        services_list = []
        services_dict = {}
        total_customers = 0
        total_income = 0
        for service in services:
            name = service.name
            id = service.id
            invoice = Invoice.objects.filter(date_of_services__gte=timezone.now().replace(
            hour=0, minute=0, second=0), date_of_services__lte=timezone.now().replace(hour=23, minute=59, second=59),branch='fourways',service=id)
            total_count =  invoice.count()
            total_amount = sum([i.Total for i in invoice])
            total_customers += total_count
            total_income += total_amount
            services_dict = {'name':name, 'total_count':total_count, 'total_amount':total_amount}
            services_list.append(services_dict)

        context = {'services_list':services_list,'today':today, 'total_customers':total_customers,
                    'sales_amount':sales_amount,'sales_count':sales_count,'total_income':total_income}

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

# monthly Reports
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def OverallMonthlyReport(request):
    current_month = datetime.now().month
    sales = Sale.objects.filter(date_of_sale__month=current_month)
    sales_amount = sum([i.amount for i in sales])
    sales_count = sales.count()
    current_mon = datetime.now().strftime("%B")
    services = Service.objects.all()
    services_list = []
    services_dict = {}
    total_customers = 0
    total_income = 0
    for service in services:
        name = service.name
        id = service.id
        invoice = Invoice.objects.filter(date_of_services__month=current_month,service=id)
        total_count =  invoice.count()
        total_amount = sum([i.Total for i in invoice])
        total_customers += total_count
        total_income += total_amount
        services_dict = {'name':name, 'total_count':total_count, 'total_amount':total_amount}
        services_list.append(services_dict)

    context = {'services_list':services_list, 'current_month':current_mon, 
        'total_customers':total_customers,'total_income':total_income,
        'sales_amount':sales_amount,'sales_count':sales_count}

    return render(request, 'reports/overall_monthly_report.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class OVERALLMONPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/overall_monthly_report_pdf.html')
        today = datetime.now()
        current_month = datetime.now().month
        sales = Sale.objects.filter(date_of_sale__month=current_month)
        sales_amount = sum([i.amount for i in sales])
        sales_count = sales.count()
        current_month = datetime.now().month
        sales = Invoice.objects.filter(date_of_services__month=current_month)
        current_mon = datetime.now().strftime("%B")
        services = Service.objects.all()
        services_list = []
        services_dict = {}
        total_customers = 0
        total_income = 0
        for service in services:
            name = service.name
            id = service.id
            invoice = Invoice.objects.filter(date_of_services__month=current_month,service=id)
            total_count =  invoice.count()
            total_amount = sum([i.Total for i in invoice])
            total_customers += total_count
            total_income += total_amount
            services_dict = {'name':name, 'total_count':total_count, 'total_amount':total_amount}
            services_list.append(services_dict)

        context = {'services_list':services_list, 'current_month':current_mon, 
                    'sales_amount':sales_amount,'sales_count':sales_count,
                    'total_customers':total_customers,'total_income':total_income, 'today':today}

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
@method_decorator(admin_only, name='dispatch')
class PreviousOVERALLPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reports/previou_mon_overall_report.html')
        current_month = datetime.now().month - 1
        previous_month = date.today().replace(day=1) - timedelta(1)
        previous_month.strftime("%B")
        sales = Sale.objects.filter(date_of_sale__month=current_month)
        sales_amount = sum([i.amount for i in sales])
        sales_count = sales.count()
        current_mon = datetime.now().strftime("%B")
        services = Service.objects.all()
        services_list = []
        services_dict = {}
        total_customers = 0
        total_income = 0
        for service in services:
            name = service.name
            id = service.id
            invoice = Invoice.objects.filter(date_of_services__month=current_month,service=id)
            total_count =  invoice.count()
            total_amount = sum([i.Total for i in invoice])
            total_customers += total_count
            total_income += total_amount
            services_dict = {'name':name, 'total_count':total_count, 'total_amount':total_amount}
            services_list.append(services_dict)

        context = {'services_list':services_list, 'previous_month':previous_month, 
                    'total_customers':total_customers,'total_income':total_income,
                    'sales_amount':sales_amount,'sales_count':sales_count}


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


#Customers
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def CustomerList(request):
    customer = Customer.objects.all()
    myFilter = CustomerFilter(request.GET, queryset=customer)
    customer = myFilter.qs
    paginator = Paginator(customer, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'customer': customer, 'page_obj': page_obj,'myFilter':myFilter}

    return render(request, 'customers/customers_list.html', context) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def CustomerHistory(request, name):
    customer = Customer.objects.get(name=name)
    invoice = Invoice.objects.filter(customer=customer)
    myFilter = CustomerHistoryFilter(request.GET, queryset=invoice)
    invoice = myFilter.qs

    paginator = Paginator(invoice, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'invoice':invoice, 'customer':customer, 'page_obj':page_obj, 'myFilter':myFilter}

    return render(request, 'customers/customer_history.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def CustomerSalesHistory(request, name):
    customer = Customer.objects.get(name=name)
    sales = Sale.objects.filter(customer=customer)
    myFilter = CustomerSalesHistoryFilter(request.GET, queryset=sales)
    invoice = myFilter.qs

    paginator = Paginator(invoice, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'sales':sales, 'customer':customer, 'page_obj':page_obj, 'myFilter':myFilter}

    return render(request, 'customers/customer_sales_history.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('customer_list')
    context = {'form':form}
    return render(request, 'customers/add_customer.html',context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Products(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all().order_by('name')
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {'products': products,
               'cartItems': cartItems, 'page_obj': page_obj, 'myFilter': myFilter}
    return render(request, 'products/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def cartPage(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart/cart.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form':form}
    return render(request, 'products/add_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def salesList(request):
    sales = Sale.objects.all().order_by('date_of_sale')
    myFilter = SalesFilter(request.GET, queryset=sales)
    sales = myFilter.qs

    paginator = Paginator(sales, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {'sales':sales, 'page_obj':page_obj}
    return render(request, 'products/sales_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addSales(request):
    form = SalesForm()

    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales')
    
    context = {'form':form}
    return render(request, 'products/add_sales.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addService(request):
    form = ServiceForm()

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    
    context = {'form':form}
    return render(request, 'invoice/add_service.html', context)
