from fanfou.profiles.models import Profile
from django.shortcuts import render_to_response, get_object_or_404,redirect
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import PasswordResetForm,PasswordChangeForm,AdminPasswordChangeForm
from forms import *
from fanfou.dynamicresponse.response import *
import pdb
from django.views.generic.create_update import *

def create_user(request,):
    """ creates a users."""
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            return HttpResponseRedirect(reverse(editer_profile,args=[user] ))
    else: 
        form=UserCreationForm()
#  return render_to_response("registration/register.html",{"form":form,})
    return render_to_response('profiles/create_user.html', { 'form': form })
def editer_profile(request, username):
    form = ProfileForm
    if username:
        user=get_object_or_404(User, username=username)
    #pdb.set_trace()
    if request.method == 'POST':

        form = ProfileForm(request.POST,instance=user)
        if form.is_valid():
            ct=form.cleaned_data
            form.save()
            #user.get_profile().
            return HttpResponseRedirect(reverse(display_profile,args=[user] ))
            
    else:
        
        form = ProfileForm(instance=user)
    
    return render_to_response('profiles/profile_edite.html',{ 'form': form,'user':user })

def display_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render_to_response("profiles/profile_show.html", { 'user':user })
def passwordchange(request, username=None):
    password_change_form=PasswordChangeForm
    #pdb.set_trace()
    if username:
        #user = get_object_or_404(User.objects.get(id=user_id), pk=user_id)
        user = get_object_or_404(User.objects.get(username=username),username=username)
    else:
        user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('home'))
            
    else:
        
        form = password_change_form(user)
    
    return render_to_response('profiles/create_user.html', { 'form': form,'user': user })
