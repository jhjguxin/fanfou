#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from fanfou.apps.meal.models import Order,Restaurant
class OrderAdmin(admin.ModelAdmin):
    list_display=('user','guests','article','price','total','date')
class RestaurantAdmin(admin.ModelAdmin):
    list_display=('article','date','hoter')
admin.site.register(Order,OrderAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
