from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from fanfou.views import *
from django.views.static import serve
from django.contrib.auth.views import login,logout
admin.autodiscover()
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
#from fanfou.apps.fanfou.models import Article
import os, sys

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

static = os.path.join(
    os.path.dirname(__file__), 'static'
)
media = os.path.join(
    os.path.dirname(__file__), 'media'
)
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'fanfou.views.home', name='home'),
    #url(r'^fanfou/', include('fanfou.urls')),

)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^meal/', include('apps.meal.urls')),
    url(r'^fanfou/', include('apps.fanfou.urls')),
    url(r'^login',login,{"template_name":'profiles/login.html'},name='login'),
    url(r'^logout/$', logout,{"template_name":'profiles/logout.html'},name='logout'),

	    # Images, Css, etc...
	    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static }),
	    (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media }),
    )
