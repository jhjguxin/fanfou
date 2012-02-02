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
from fanfou.apps.fanfou.forms import Traded_articleForm
from fanfou.apps.meal.models import Order,Restaurant
from fanfou.apps.fanfou.models import Category,Article,Traded_article
import datetime
import calendar
import pdb

def placeOrder(request):
    late = False
    todays_orders = False
    #pdb.set_trace()
    if request.user.is_anonymous():
        #return redirect_to_login('/',login_url="/login")
        return HttpResponseRedirect(urlreverse('login'))
    else:
        #pdb.set_trace()#this time late
        d=datetime.date.today()
        #read today's menue if you want render the aritcle with mult category your can query category and send to templates
        today_article=Article.objects.filter(category__status=1)
        if datetime.datetime.now()>datetime.datetime(d.year,d.month, d.day, 10, 25, 0,0):
            late=True
            # if lunch was already submitted today...
        todays_orders = Traded_article.objects.filter(author=request.user,created_on__year=d.year,created_on__month=d.month,created_on__day=d.day)
        #pdb.set_trace()
        if todays_orders.exists():
            todays_orders = True

        if request.method == 'POST' and (todays_orders and not late):
            Traded_article.objects.filter(author=request.user,created_on__year=d.year,created_on__month=d.month,created_on__day=d.day).delete()
            return HttpResponseRedirect(urlreverse('f_order'))
            
    
        if request.method == 'POST' and not late: # If the form has been submitted...
            #request.META['REMOTE_HOST']
            #pdb.set_trace()

            if request.POST.has_key('order'):
                a=Article.objects.filter(id=request.POST.get('order'))
                if a.exists():
                    #pdb.set_trace()
                    form = Traded_articleForm(request.POST, instance=Traded_article(author=request.user,article=a[0],pc=request.META['REMOTE_ADDR'],)) # A form bound to the POST data
                    if form.is_valid(): # All validation rules pass
                        # Process the data in form.cleaned_data
                        #pdb.set_trace()
                        form.save()
                        return HttpResponseRedirect(urlreverse('f_thanksorder')) # Redirect after POSTthanksorder
            form = Traded_articleForm() # An unbound form
        else:
            form = Traded_articleForm() # An unbound form

        return render_to_response('fanfou/orderform.html',
                               {'form': form, 'username' : request.user.username, 'late': late,"todays_orders":todays_orders,'articles':today_article },
                              context_instance=RequestContext(request))

def thanks(request):
  return render_to_response("meal/thanks.html",{ 'user': request.user })

def viewOrders(request, date=None,summary=None):
    #pdb.set_trace()
    if request.GET.has_key('date'):
      if request.GET['date']==u'today':  date = datetime.datetime.now()
    #if date=='today':  date = datetime.datetime.now()
    if request.GET.has_key('summary'):
      if request.GET['summary']==u'true':  summary=True

    if date:
        orders = Traded_article.objects.filter(created_on__year=date.year,created_on__month=date.month,created_on__day=date.day).all().order_by("created_on").reverse()
        if summary:
            orders=articleorder(orders)
    else:
        #orders = Traded_article.objects.all()
        orders = Traded_article.objects.all().order_by("created_on").reverse()
        if summary:
            orders=articleorder(orders)
    #total = reduce(lambda x,y: 1,orders,0)
    #pdb.set_trace()
    atotal=0
    for order in orders:
        #pdb.set_trace()
        atotal += order.total



    return render_to_response('fanfou/vieworders.html',{'orders':orders, 'atotal':atotal,'user': request.user})

def articleorder(orders=Traded_article.objects.all()):
    #pdb.set_trace()
    orders_list=list(orders.reverse())
    orders_list1=list(orders)
    #old_order=orders[0]
    new_orders=[]
    for old_order in orders_list:
        #pdb.set_trace()
        for d in orders_list1:
            d.author.username='summaryshow'
            if (d.article_id==old_order.article_id) and (d.id != old_order.id):
                #pdb.set_trace()

                d.guests=d.guests+(1+old_order.guests)
                d.total= d.article.price*(d.guests+1)
                try :
                    orders_list1.remove(old_order)
                except:
                    pass



        #old_order.total= old_order.article.price*(old_order.guests+1)
        #new_orders.append(old_order)
        #orders_list.remove(old_order)        


#pdb.set_trace()
    orders_list1.reverse()
    return orders_list1

def viewOrdersSummary(request, year=None, month=None):
    year = int(year)  if year is not None else  datetime.datetime.now().year
    month = int(month)  if month is not None else  datetime.datetime.now().month
    
    # get all months & years in the db
    #pdb.set_trace()
    values_list = Traded_article.objects.values_list('created_on', flat=True)
    unique_dates = set(
        val.replace(day=1) for val in values_list if isinstance(val, datetime.datetime)
        )
    # also include the current month
    unique_dates.add(datetime.datetime.now().replace(day=1))
    unique_dates = list(unique_dates)
    unique_dates.sort(reverse=True)
    oldtime=unique_dates[0]
    new_dates=[unique_dates[0]]
    for d in unique_dates:
        if not(d.year==oldtime.year and d.month==oldtime.month):
            new_dates.append(d)
            #type(d)
            oldtime=d
            #unique_dates.remove(d)
    #pdb.set_trace()
    unique_dates=new_dates
         


    # date info to pass to html template
    dateslist = list(
                {'title': d.strftime('%b %Y'), 
                 'val': urlreverse('lunch-summary-view', kwargs={'year':d.year,'month':d.month}), 
                 'selected': d.month==month and d.year==year} 
            for d in unique_dates)
    
    # orders for given month and year
    orders = Traded_article.objects.filter(created_on__year=year,created_on__month=month)
    
    usertotals = []
    grandtotal = sum((ord.guests+1) for ord in orders)
    
    for user in User.objects.all():
        uorders = orders.filter(author=user)
        usertotal = {}
        usertotal['user'] = user
        t = sum((ord.guests+1) for ord in uorders)
        usertotal['sum'] = t
        usertotal['percent'] = 0.  if grandtotal==0 else  100.*t/float(grandtotal)
        usertotals.append(usertotal)
    
    return render_to_response('fanfou/orders_summary.html',
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
    
    
    
    
    
