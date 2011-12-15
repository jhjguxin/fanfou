from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as urlreverse
#from django.core.urlresolvers import reverse
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import login,logout,redirect_to_login

from fanfou.apps.meal.forms import OrderForm
from fanfou.apps.meal.models import Order,Restaurant

import datetime
import calendar
import pdb

def placeOrder(request):
    sameday = False
    #pdb.set_trace()
    if request.user.is_anonymous():
        #return redirect_to_login('/',login_url="/login")
        return HttpResponseRedirect(urlreverse('login'))
    else:

        # if lunch was already submitted today...
        todays_orders = Order.objects.filter(user=request.user,date=datetime.date.today())
        if todays_orders.exists():
            sameday = True
    
        if request.method == 'POST' and not sameday: # If the form has been submitted...
            #request.META['REMOTE_HOST']
            #pdb.set_trace()
            form = OrderForm(request.POST, instance=Order(user=request.user,pc=request.META['REMOTE_ADDR'],total=request.POST.get('total'))) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                #pdb.set_trace()
                form.save()
                return HttpResponseRedirect(urlreverse('thanksorder')) # Redirect after POSTthanksorder
        else:
            form = OrderForm() # An unbound form

        return render_to_response('meal/orderform.html',
                               {'form': form, 'username' : request.user.username, 'sameday': sameday },
                              context_instance=RequestContext(request))

def thanks(request):
  return render_to_response("meal/thanks.html",{ 'user': request.user })

def viewOrders(request, date=None):
    if date=='today':  date = datetime.date.today()
    if date:
        orders = Order.objects.filter(date=date).all()
    else:
        orders = Order.objects.all()
    #total = reduce(lambda x,y: 1,orders,0)
    #pdb.set_trace()
    atotal=0
    for order in orders:
      #pdb.set_trace()
      atotal += order.total
    return render_to_response('meal/vieworders.html',{'orders':orders, 'atotal':atotal,'user': request.user})


def viewOrdersSummary(request, year=None, month=None):
    year = int(year)  if year is not None else  datetime.date.today().year
    month = int(month)  if month is not None else  datetime.date.today().month
    
    # get all months & years in the db
    values_list = Order.objects.values_list('date', flat=True)
    unique_dates = set(
        val.replace(day=1) for val in values_list if isinstance(val, datetime.date)
        )
    # also include the current month
    unique_dates.add(datetime.date.today().replace(day=1))
    unique_dates = list(unique_dates)
    unique_dates.sort(reverse=True)
    
    # date info to pass to html template
    dateslist = list(
                {'title': d.strftime('%b %Y'), 
                 'val': urlreverse('lunch-summary-view', kwargs={'year':d.year,'month':d.month}), 
                 'selected': d.month==month and d.year==year} 
            for d in unique_dates)
    
    # orders for given month and year
    orders = Order.objects.filter(date__year=year,date__month=month)
    
    usertotals = []
    grandtotal = sum((ord.guests+1) for ord in orders)
    
    for user in User.objects.all():
        uorders = orders.filter(user=user)
        usertotal = {}
        usertotal['user'] = user
        t = sum((ord.guests+1) for ord in uorders)
        usertotal['sum'] = t
        usertotal['percent'] = 0.  if grandtotal==0 else  100.*t/float(grandtotal)
        usertotals.append(usertotal)
    
    return render_to_response('meal/orders_summary.html',
                             {'usertotals':usertotals, 'month':calendar.month_name[month], 
                              'year':year, 'grandtotal':grandtotal,
                              'dateslist':dateslist,'user': request.user}
                             )
    
def logout(request):
    django_logout(request)
    return HttpResponse('Logout successful.')
    
def restaurant_detail(request,year,month,day,id):

    restaurant=Restaurant.objects.get(id=id)
    restaurant.hoter=float(int(restaurant.hoter)+1)
    restaurant.save()

    return render_to_response('meal/restaurant_detail.html', {"restaurant": restaurant,'user': request.user})
    
    
    
    
    
