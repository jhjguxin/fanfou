#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import PasswordResetForm,PasswordChangeForm,AdminPasswordChangeForm,UserChangeForm
import pdb
import datetime
from fanfou.profiles.models import Profile
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class ProfileForm(UserChangeForm):
    """Creates/updates a blog post."""
    #tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all()) 

    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email',)
#('id','first_name','last_name','gender','mugshot','signature','birthday','phone',)
#        fields = ('id','title','author','tag','categories','content','hoter',)
class U_PasswordChangeForm(PasswordChangeForm):
    """updates a blog user."""
    
    class Meta:
        model = User
        fields = ('id','old_password','password1','password2',)
