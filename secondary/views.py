from django.shortcuts import render
from primary.models import Product,Collection,OrderItem,Order,Customer
from django.db.models import Q,F,Value
from django.db.models.aggregates import Count,Max,Min,Avg,Sum
from django.db.models.functions import Concat


def hello(request):
    # queryset=OrderItem.objects.annotate(Total_price=Sum(F('quantity')*F('product__unit_price')))
    # queryset=OrderItem.objects.annotate(product_unit_priceS=F('product__unit_price'))
    # queryset=Customer.objects.annotate(fullname=Concat('first_name',Value(" "),'last_name'))
    # queryset=Customer.objects.annotate(Total_spending=Sum(F('order__order_items__unit_price')*F('order__order_items__quantity')))
    queryset=Product.objects.annotate(Total_sales=Sum(F('orderitem__unit_price')*F('orderitem__quantity'))).order_by('Total_sales')[0:5]

    print(queryset)
    
    return render(request,'hello.html',{'result':queryset})
