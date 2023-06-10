from django.shortcuts import render
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, OrderItem, Order


def say_hello(request):
    
    # Each model we create has the attribute 'objects.' which returns a manager that can iteract with the database.
    # '.all', like most of the 'objects.' methods, returns a query set that is not yet evaluated. In contrast when you
    # iterate through the query, turn it into a list, or access an individual element it returns a result immediately
    #query_set = Product.objects.all()
    #list(query_set)
    #query_set[0:5]

    # Pay attention if your function returns an actual object or a query set and name your variable accordingly.
    #query_set = Product.objects.all()
    #product = Product.objects.get(id=1)
    #product = Product.objects.get(pk=1)

    # When you run an error enducing query you can use a try catch block along with 'ObjectDoesNotExist' to
    # return a error message.
    #try:
    #    product = Product.objects.get(pk=0)
    #except ObjectDoesNotExist:
    #    pass

    # When an error is returned and we want to avoid using 'try' we can add the '.first' operator to have it return None
    #product = Product.objects.filter(pk=0).first()

    # We can also check if something exists, remember that it returns a boolean statement and to plan accordingly
    #exists = Product.objects.filter(pk=0).exists()

    # Filtering data does not take logical operators, instead we need to look up a kew word value. Look up query set
    # api for Django to find the documentation for field lookups. Below is the example for 'greater than'
    #query_set = Product.objects.filter(unit_price__gt=20)

    # Understand that when you decide to run a filter you must also specify where the 
    #query_set = Customer.objects.filter(first_name__icontains='.com')
    #query_set = Collection.objects.filter(featured_product__isnull=True)
    #query_set = Product.objects.filter(inventory__lt=10)
    #query_set = Order.objects.filter(customer__id=1)
    #query_set = OrderItem.objects.filter(product__collection__id=3)
    #query_set = OrderItem.objects.filter(order__customer__id=1)

    # For the 'and' operator you may use any of the meathods below
    #query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    #query_set

    #query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    #query_set = Product.objects.filter(inventory=F('unit_price'))


    # Since a query set is returned you must convert it to a list. 
    return render(request, 'hello.html', {'name': 'Mosh', 'products': list(query_set)})
