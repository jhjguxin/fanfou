#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from fanfou.apps.fanfou.models import Category,Article,Traded_article
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','call','status','notes')
    actions = ['make_published','make_draft','make_hidden',]

    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        #pdb.set_trace()
        #super(PostAdmin, self)
        #qs = self.model.live
        qs = super(CategoryAdmin, self).queryset(request).model.objects.all()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = super(CategoryAdmin, self).ordering
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def make_published(self, request, queryset):
        rows_updated = queryset.update(status=1)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    def make_draft(self, request, queryset):
        rows_updated = queryset.update(status=2)
        if rows_updated == 2:
            message_bit = "2 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as draft." % message_bit)

    def make_hidden(self, request, queryset):
        rows_updated = queryset.update(status=3)
        if rows_updated == 3:
            message_bit = "3 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as hidden." % message_bit)



class ArticleAdmin(admin.ModelAdmin):
    list_display=('name','category','price','created_on')
    list_filter = ('category__status','category',"price",'category__call')
    search_fields = ('name','category__name',"price",'created_on',)
class Traded_articleAdmin(admin.ModelAdmin):
    list_display=('author','guests','article','total','pc','created_on',)
    list_filter = ('author', 'article__category', "created_on")
    search_fields = ('author__username','category__name','^author__first_name', '^author__last_name',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Traded_article,Traded_articleAdmin)
