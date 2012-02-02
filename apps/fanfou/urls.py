from django.conf.urls.defaults import *
from fanfou.apps.fanfou.models import Category,Article,Traded_article
import datetime

category_display_dict = {
    'queryset' : Category.objects.all(),
    'template_object_name': 'restaurants',
#    'template_name' : 'blog/category_detail.html',#default setting template_name category_detail.html
}


urlpatterns = patterns('fanfou.apps.fanfou',
    url(r'^order/$', 'views.placeOrder',name='f_order'),
    url(r'^$', 'views.placeOrder'),
    #(rs'^logout/$', django.contrib.auth.views.logout_then_login),
    #(r'^logout/$', 'views.logout'),
    url(r'^thanks/$', 'views.thanks',name='f_thanksorder'),
    url(r'^orders/', 'views.viewOrders',name='f_orderlist'),
    url(r'^orders/(?P<date>(\d{4}-\d{2}-\d{2}){1})/$', 'views.viewOrders'),
    url(r'^summary/$', 'views.viewOrdersSummary',name='f_summary' ),
    url(r'^summary/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'views.viewOrdersSummary', {}, 'lunch-summary-view'),
    url(r'^(?P<year>(\d){4})/(?P<month>(\d){2})/(?P<day>(\d){2})/(?P<id>[\d]+)/$', 'views.restaurant_detail', name="f_restaurant_detail"),
)



urlpatterns += patterns('django.views.generic.list_detail',
    
    # Display Article in Category
    url(r'^(?P<slug>[-\w]+)/$', 'object_detail', category_display_dict, name="category_detail"),
    
)

