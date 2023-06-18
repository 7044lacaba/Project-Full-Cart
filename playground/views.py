from django.shortcuts import render
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Product, Customer, Collection, OrderItem, Order


def say_hello(request):
    
    # Each model we create has the attribute 'objects.' which returns a manager that can iteract with the database.
    # '.all', like most of the 'objects.' methods, returns a query set that is not yet evaluated. In contrast when you
    # iterate through the query, turn it into a list, or access an individual element it returns a result immediately
    query_set = Product.objects.all()
    #list(query_set)
    #query_set[0:5]

    # Pay attention if your function returns an actual object or a query set and name your variable accordingly.
    query_set = Product.objects.all()
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
    query_set = Product.objects.filter(unit_price__gt=20)

    # Understand that when you decide to run a filter you must also specify where the 
    query_set = Customer.objects.filter(first_name__icontains='.com')
    query_set = Collection.objects.filter(featured_product__isnull=True)
    query_set = Product.objects.filter(inventory__lt=10)
    query_set = Order.objects.filter(customer__id=1)
    query_set = OrderItem.objects.filter(product__collection__id=3)
    query_set = OrderItem.objects.filter(order__customer__id=1)

    # For the 'and' operator you can use either of the meathods below
    query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    # For the 'or' operator you can use either of the meathods below (import Q)
    query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

    # For the 'not' operator you can use you use '~'
    query_set = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))

    # To compare two feilds we can use F objects, additionally we can also referance a related table
    query_set = Product.objects.filter(inventory=F('unit_price'))
    query_set = Product.objects.filter(inventory=F('collection__id'))

    # In terms of sorting we can order things with the 'order_by' operator, we can add a '-' to have it in decending order
    # additionally we can sort with multiple feilds, shown in the second example. The second example sorts the results by
    # unit price in asc order and if there are multiple with the same price its then sorted by title in des order. Adding
    # a '.reverse' opperator reverses all of that. 
    query_set = Product.objects.order_by('title')
    query_set = Product.objects.order_by('unit_price', '-title')
    query_set = Product.objects.order_by('unit_price', '-title').reverse

    # Collection with id 1 sorted by unit price 
    query_set = Product.objects.filter(collection__id=1).order_by('unit_price')

    # By asking for the first element in the list you convert the query set into an actual object, dont forget 
    # to properly rename the variable and to remove the 'list()' operator from your return 
    #product = Product.objects.order_by('unit_price')[0]

    # We can also use '.earliest', this also returns an object
    #product = Product.objects.earliest('unit_price')
    #product = Product.objects.latest('unit_price')

    # We can also splice the query set
    query_set = Product.objects.all()[:5]

    # When you want specific collumns from a table, this returns a dictionary
    query_set = Product.objects.values('id', 'title', 'collection__title')

    # On the other hand '.values_list' returns a touple of the values for each key
    query_set = Product.objects.values_list('id', 'title', 'collection__title')

    # This is how you reverse query in Django, you wrap an query ina query that checks the linking id.
    query_set = OrderItem.objects.filter(order_id__gt=0).order_by('product__title')
    query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    # Use '.defer' and '.only' like '.value' but note that it locks out the coloumns and asking for thoes said 
    # coloumns later will cause an individual query every time we want to access the locked coloumns
    query_set = Product.objects.only('id', 'title')
    query_set = Product.objects.defer('id', 'title')

    # This selects all from both and 'inner join' at related point (Product is main table, then put the bridge table in 
    # quotes, you can also link more by adding double underscore)
    # select_related (1) - product has one collection - one to one 
    query_set = Product.objects.select_related('collection').all()
    query_set = OrderItem.objects.select_related('product__collection').all()

    # prefetch_related (n) - product has many promotions - one to many
    query_set = Product.objects.prefetch_related('promotions').all()

    # You can link the two concepts together
    query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()

    # Problem
    query_set = Order.objects.prefetch_related('orderitem_set__product').select_related('customer').order_by('-placed_at')[:5]

    # Count using the primary key/'id', if you use something like 'description' it will count each and skip over any 
    # values that are null. This doesnt return a query set but rather a dictionary, to access the answer the key will 
    # be 'id__count'
    #result = Product.objects.aggregate(Count('id'))

    # To change the key name store it into a variable with the desired name
    #result = Product.objects.aggregate(count_1=Count('id'))

    # Since aggregate is a meathod of query sets you can apply it to wherever you have a query set.
    #result = Product.objects.filter(collection__id=1).aggregate(count_1=Count('id'), min_price=Min('unit_price'))

    # Problems
    result = Order.objects.aggregate(Count('id'))

    


    # Since a query set is returned you must convert it to a list. 
    return render(request, 'hello.html', {'name': 'Mosh', 'result': result})
