from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import*

def signup(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        full_name=request.POST['full_name']
        email=request.POST['email']
        # phone_number=request.POST['phone_number']

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username allready exist')
            print("username allready exist hello")
            return redirect('signup')
        
        user=User.objects.create_user(username=username,password=password,email=email)
        user.first_name=full_name
        # user.profile.phone_number = phone_number
        user.save()
        messages.success(request,f'account created succesfull {username}!')
        return redirect('login')
    return render(request,'accounts/signup.html')

def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:   
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,'invalid username or password')
    
    return render(request,'accounts/login.html')

def additem_view(request):
    if request.method=='POST':
        item_name=request.POST['item_name']
        item_size=request.POST['item_size']
        item_category=request.POST['item_category']
        item_count=int(request.POST['item_count'])
        item_price=int(request.POST['item_price'])
        profit, created=Profit.objects.get_or_create(id=1)
        profit.total_expenses_on_clothes+=item_price
        user_name=request.user
        additem=AddItem.objects.create(
            user_name=user_name,
            item_name=item_name,
            item_size=item_size,
            item_category=item_category,
            item_count=item_count,
            item_price=item_price
        )
        profit.save()
        if Item.objects.filter(item_name=item_name,item_size=item_size,item_category=item_category).exists():
            item = Item.objects.get(item_name=item_name, item_size=item_size, item_category=item_category)
            a1=item.item_price*item.item_count
            a2=item_count*item_price
            item.item_count+=item_count
            item.item_price=int((a1+a2)/item.item_count)
            item.save()
        
        else:
            item=Item.objects.create(item_name=item_name,
                                     item_size=item_size,
                                     item_category=item_category,
                                     item_count=item_count,
                                     item_price=item_price)
        return redirect('/')
    return render(request,'additem.html')


def home(request):
    item=Item.objects.all().order_by('item_category')
    return render(request,'home.html',{'items_with_prices':item})

def logout_view(request):
    logout(request)
    return render(request, 'home.html', {'message': 'You have been logged out successfully!'})
    # return redirect('/')

@login_required(login_url='/login/')
def sale_item(request, item_id):
    # Use get_object_or_404 to handle cases where the item with the given id does not exist
    item = get_object_or_404(Item, id=item_id)

    if request.method=='POST':
        quantity_sold=int(request.POST['quantity_sold'])
        selling_price_online=int(request.POST['selling_price_online'])
        selling_price_offline=int(request.POST['selling_price_offline'])
        cur_count=item.item_count
        if cur_count>=quantity_sold:
            profit,created=Profit.objects.get_or_create(id=1)
            profit.gross_earning+=(selling_price_online+selling_price_offline)
            profit.gross_profit+=(selling_price_offline+selling_price_online-item.item_price*quantity_sold)
            profit.cur_amount_on_bank+=selling_price_online
            profit.cur_amount_on_counter+=selling_price_offline
            profit.save()
            payment_mode=request.POST['payment_mode']
            item.item_count-=quantity_sold
            item.save()
            user_name=request.user
            transactions=Transactions.objects.create(
                item=item,
                quantity_sold=quantity_sold,
                selling_price_online=selling_price_online,
                selling_price_offline=selling_price_offline,
                payment_mode=payment_mode,
                sold_by=user_name,
                sale_profit=(selling_price_offline+selling_price_online-quantity_sold*item.item_price)
            )
            return redirect('/')
        else:
            messages.error(request,'Quantity not available {cur_count}')

    context = {
        'item_name': item.item_name,
        'item_size': item.item_size,
        'item_category': item.item_category,
        'item_count': item.item_count,
    }

    return render(request, "sale_item.html", {'context':context})

def transaction_view(request):
    transaction=Transactions.objects.all()
    return render(request,"transaction.html",{'context':transaction})

def profit_view(request):
    profit=Profit.objects.all()
    return render(request,"profit.html",{'context':profit})

@login_required(login_url='/login/')
def expenses_view(request):
    if request.method=='POST':
        user_name=request.user
        expenses_on=request.POST['expenses_on']
        expenses_mode=request.POST['expenses_mode']
        expense_online=int(request.POST['expenses_online'])
        expense_offline=int(request.POST['expenses_offline'])
        profit,created=Profit.objects.get_or_create(id=1)
        if profit.cur_amount_on_bank>=expense_online and profit.cur_amount_on_counter>=expense_offline :
            profit.cur_amount_on_bank-=(expense_online)
            profit.cur_amount_on_counter-=(expense_offline)
            if expenses_on=="Shop":
                profit.total_expenses_on_shop+=(expense_offline+expense_online)
            if expenses_on=="Shopkeeper":
                profit.total_expenses_on_shopkeeper+=(expense_offline+expense_online)
            if expenses_on=="Other":
                profit.total_expenses_on_other+=(expense_offline+expense_online)
            profit.save()
            expenses=Expenses.objects.create(
                user_name=user_name,
                expenses_on=expenses_on,
                expenses_mode=expenses_mode,
                expenses_online=expense_online,
                expenses_offline=expense_offline
            )
        else :
            messages.error(request,'we do not have that much of money')
        return redirect('/')
    return render(request,"expenses.html")

def expenses_history_view(request):
    expenses_history=Expenses.objects.all()
    return render(request,"expenses_history.html",{'context':expenses_history})

def additem_history_view(request):
    additem=AddItem.objects.all()
    return render(request,"additem_history.html",{'context':additem})