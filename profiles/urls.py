from django.conf.urls.defaults import *
from fanfou.profiles.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.views import login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm,PasswordChangeForm,AdminPasswordChangeForm

create_user_dict = {
    'model': User,
    'template_name': 'profiles/create_user.html',
    'form_class':UserCreationForm,
    'post_save_redirect':'update_profile',
}



update_profile_dict = {
    'model': Profile,
    'template_object_name': 'profile',
    'login_required':True,
}

urlpatterns = patterns('fanfou.profiles.views',
    url(r'^create', 'create_user', name='create_user'),
    url(r'^(?P<username>[-\w]+)/$', 'display_profile', name='display_profile'),
    url(r'^(?P<username>[-\w]+)/passwordchange/$', 'passwordchange', name='passwordchange'),

    url(r'^(?P<username>[-\w]+)/edite$', 'editer_profile',name='update_profile'),
)
#urlpatterns += patterns ('django.views.generic.create_update',
    #url(r'^create', 'create_object',create_user_dict, name='create_user'),
    #url(r'^(?P<username>[-\w]+)/passwordchange/$', 'update_object', change_password_dict, name='passwordchange'),
#)
