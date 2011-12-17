#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.comments.signals import comment_will_be_posted
from django.contrib.comments.models import Comment
from fanfou.apps.fanfou.managers import LiveCategoryManager
from markdown import markdown
import settings

import pdb

class Category(models.Model):
  LIVE_STATUS = 1
  DRAFT_STATUS = 2
  HIDDEN_STATUS = 3
        
  STATUS_CHOICE = (
                (LIVE_STATUS, 'Live'),
                (DRAFT_STATUS, 'Draft'),
                (HIDDEN_STATUS,'Hidden'),
             )
  name=models.CharField(max_length=255,help_text=_(u'Name of the restaurant.'))
  status = models.IntegerField(_('status'),choices=STATUS_CHOICE,help_text=_('The status of this restaurant.'))  
  call=models.IntegerField(default=110,help_text=_(u'phonenumber of the restaurant.'))
  notes=models.CharField(max_length=255,blank=True,help_text=_(u'Introduction of the restaurant.'))
  slug=models.SlugField(unique=True)

  objects = models.Manager()
  live=LiveCategoryManager()

  def __unicode__(self):
    return self.name
            
  class Meta:
    ordering = ['name']
    verbose_name_plural = "categories"
        
  @models.permalink
  def get_absolute_url(self):
    return('category_detail', (), {'slug': self.slug })

class Article(models.Model):
  "the class of article"
  name=models.CharField(max_length=30,help_text=_(u'Name of the article.'))
  category = models.ForeignKey(Category,help_text=_(u'Provide by which restaurant.'))
#  image=models.ImageField('Article',upload_to= settings.MEDIA_ROOT)
  price=models.FloatField(default=0.0,help_text=_(u'The unit price.'))
  notes=models.CharField(max_length=30,blank=True,help_text=_(u'Introduction of the article.'))
  created_on = models.DateTimeField(auto_now_add=True,editable=False)
  date_modified = models.DateTimeField(auto_now_add=True, editable=False)
  def serialize_fields(self):
    """Only these fields will be included in API responses."""
    return [
           'id',
            'name',
            'category',
            'price',
            'notes',
            'created_on',
            'date_modified',
]
  def __unicode__(self):
    return '%s in %s price: %s' % ( self.name,self.category.name, self.price)
  def __str__(self):
    return '%s in %s price: %s' % ( self.name,self.category.name, self.price)

  def __repr__(self):
    return '%s in %s price: %s' % ( self.name,self.category.name, self.price)


class Traded_article(models.Model):
  author = models.ForeignKey(User,help_text=_(u'who order the meal.'))
  guests = models.IntegerField(default=0,help_text=_(u'Do you have some guests? Or you want order more than one.'))
  article = models.ForeignKey(Article,help_text=_(u'Choose which you like.'))
  total = models.IntegerField(default=0,help_text=_(u'In total you should pay.'))
  notes=models.CharField(max_length=30,blank=True,help_text=_(u'There input some additional your need.'))
  pc=models.CharField(max_length=30,)
  created_on = models.DateTimeField(auto_now_add=True,editable=False)
  #date_modified = models.DateTimeField(auto_now_add=True, editable=False)

  def __str__(self):
    return '%s on %s with %s guests' % (self.author.username, self.created_on, self.guests)

  def __repr__(self):
    return '%s on %s with %s guests' % (self.author.username, self.created_on, self.guests)

  def save(self,*args, **kwargs):
    self.total= self.article.price*(self.guests+1)
    super(Traded_article, self).save() 


  def serialize_fields(self):
    """Only these fields will be included in API responses."""
    return [
           'id',
            'article',
            'author',
            'created_on',
            'date_modified',
]

# Signals
def pre_save_comment(sender, **kargs):
  """
  Run comment through a markdown filter
  """
  if 'comment' in kargs:
    comment = kargs['comment']
        
  # If in debug mode skip this check with Akismet
  if not settings.DEBUG:
    try:
      real_key = akismet.verify_key(settings.AKISMET_KEY ,Site.objects.get_current().domain)
      if real_key:
        is_spam = akismet.comment_check(settings.AKISMET_KEY ,Site.objects.get_current().domain, comment.ip_address, None, comment_content=comment.comment)
        if is_spam:
          comment.is_public = False
          print "That was spam"
    except akismet.AkismetError, e:
      print e.response, e.statuscode

  # Apply markdown
  comment.comment = markdown(comment.comment)

comment_will_be_posted.connect(pre_save_comment, Comment)
