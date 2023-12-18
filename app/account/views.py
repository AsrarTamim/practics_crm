from django.shortcuts import render,redirect

from django.http import HttpResponse
from .models import *
from .form import OrderForm
def home(request):
    order = Order.objects.all()
    customer = Customer.objects.all()
    total_customers = customer.count()
    total_orders = order.count()
    delivered = order.filter(status = 'Delivered').count()
    pending = order.filter(status = 'Pending').count()
    context = {'orders': order,'customers': customer,
                'total_orders':total_orders,'total_customers':total_customers,
                'pending':pending,'delivered':delivered
               }
    return render(request, 'account/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    return render(request, 'account/products.html',{'products': products})

def customer(request,pk_test):
    customer = Customer.objects.get(id = pk_test)
    orders = customer.order_set.all()
    order_count = orders.count
    context = {'customer':customer,'orders':orders,'order_count':order_count}
    return render(request,'account/customer.html',context)

def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
            
    context = {'form':form}
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



def updateOrder(request,pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)          
    context = {'form': form}
    return render(request,'account/order_form.html',context)