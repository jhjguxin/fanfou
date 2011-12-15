from django.conf.urls.defaults import *
from fanfou.apps.meal.models import Order,Restaurant
import datetime

index_dict = {
    'queryset': Restaurant.objects.order_by('-date'),
    'template_object_name': 'restaurant',
    'template_name': 'meal/restaurant.html',
}



urlpatterns = patterns('fanfou.apps.meal',
    url(r'^order/$', 'views.placeOrder',name='order'),
    url(r'^$', 'views.placeOrder'),
    #(rs'^logout/$', django.contrib.auth.views.logout_then_login),
    #(r'^logout/$', 'views.logout'),
    url(r'^thanks/$', 'views.thanks',name='thanksorder'),
    url(r'^orders/$', 'views.viewOrders',name='orderlist'),
    url(r'^orders/today/$', 'views.viewOrders', {'date': 'today'},name="todayorder"),
    url(r'^orders/(?P<date>(\d{4}-\d{2}-\d{2}){1})/$', 'views.viewOrders'),
    url(r'^summary/$', 'views.viewOrdersSummary',name='summary' ),
    url(r'^summary/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'views.viewOrdersSummary', {}, 'lunch-summary-view'),
    url(r'^(?P<year>(\d){4})/(?P<month>(\d){2})/(?P<day>(\d){2})/(?P<id>[\d]+)/$', 'views.restaurant_detail', name="restaurant_detail"),
)

urlpatterns += patterns ('django.views.generic.list_detail',
    # Post List
    url(r'^restaurant$', 'object_list', index_dict, name='restaurant_list'),
)

