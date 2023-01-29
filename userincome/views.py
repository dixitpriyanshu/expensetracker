from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserIncome, Source
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime
# Create your views here.


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner = request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user= request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, "income/index.html",context)

@login_required(login_url='/authentication/login')
def add_income(request):
    
    sources = Source.objects.all()
    context = {
        'sources': sources
    }

    if request.method == 'GET':
        return render(request, "income/add_income.html", context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "income/add_income.html", context)
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, " income/add_income.html", context)

        UserIncome.objects.create(owner=request.user, amount=amount, source=source, description=description, date=date)
        messages.success(request, 'Income added successfully.')
        
        return redirect('income')

@login_required(login_url='/authentication/login')
def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'sources': sources
    }
    if request.method == 'GET':        
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "income/edit_income.html", context)
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, "income/edit_income.htmll", context)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.source = source
        income.date = date

        income.save()
        messages.success(request, 'Income updated successfully.')

        return redirect('income')


def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed.')
    return redirect('income')

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days= 30*6)
    incomes = UserIncome.objects.filter(owner = request.user, date__gte = six_months_ago, date__lte = todays_date)

    finalrep = {}
    def get_source(income):
        return income.source

    def get_income_source_amount(source):
        amount = 0
        filtered_by_category = incomes.filter(source = source)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    source_list = list(set(map(get_source, incomes)))

    for income in incomes:
        for source in source_list:
            finalrep[source] = get_income_source_amount(source)

    return JsonResponse({'income_source_data': finalrep}, safe= False)

def stats_view(request):
    return render(request, 'income/stats.html')