from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .form import CustomerForm, OrderForm,CreateUserForm
from django.contrib import messages
from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_user,admin_only

@unauthenticated_user 
def registerPage(request):

    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get("username")
            
            # group=Group.objects.get(name="customer")
            # user.groups.add(group)
            # Customer.objects.create(
            #     user=user,
            #     name=form.cleaned_data.get("username"),
            #     email=form.cleaned_data.get("email")
            # )
            
            messages.success(request,"Account was created for "+username)
            return redirect("login")
    context={"form":form}
    return render(request,"account/register.html",context)

@unauthenticated_user
def loginPage(request):

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.info(request,"User name password is incorrect")
    context={}
    return render(request,"account/login.html",context)

def logoutUser(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
@admin_only
def home(request):
    order = Order.objects.all()
    customer = Customer.objects.all()
    
    total_customers = customer.count()
    total_orders = order.count()
    delivered = order.filter(status = 'Delivered').count()
    pending = order.filter(status = 'Pending').count()
    
    context = {
        'orders': order,
        'customers': customer,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'pending':pending,
        'delivered':delivered
    }
    return render(request, 'account/dashboard.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=["customer"])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context={
        'orders':orders,
        'total_orders':total_orders,
        'pending':pending,
        'delivered':delivered
        }
    return render(request,'account/user.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=["customer"])
def accountSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    
    if request.method == "POST":
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    
    context={"form":form}
    return render(request,"account/account_setting.html",context)

@login_required(login_url='login')
@allowed_user(allowed_roles=["admin"])
def products(request):
    products = Product.objects.all()
    return render(request, 'account/products.html',{'products': products})

@login_required(login_url='login')
@allowed_user(allowed_roles=["admin"])
def customer(request,pk_test):
    customer = Customer.objects.get(id = pk_test)
    orders = customer.order_set.all()
    order_count = orders.count
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs  
    context = {
        'customer':customer,
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter
        }
    return render(request,'account/customer.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=["admin"])
def createOrder(request,pk):
    orderFormSet = inlineformset_factory(Customer,Order, fields=('product','status'), extra=10)
    customer = Customer.objects.get(id = pk)
    formset = orderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = orderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
            
    context = {'formset':formset}
    return render(request,'account/order_form.html',context)

# def updateOrder(request,pk):
#     order = order.objects.get(id=pk)
    
#     form = OrderForm(instance=order)
#     if request.method == 'POST':
#         form = OrderForm(request.POST,instance=order)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
            
#     context = {'form': form}
#     return render(request,'account/order_form.html',context)


@login_required(login_url='login')
@allowed_user(allowed_roles=["admin"])
def updateOrder(request,pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)
    print(request.method)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')         
    context = {'formset': form}
    return render(request,'account/order_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=["admin"])
def deleteOrder(request,pk):
    order = Order.objects.get(id = pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request,'account/delete.html',context)