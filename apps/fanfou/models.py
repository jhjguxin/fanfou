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
from markdown import markdown
import settings

import pdb

class Category(models.Model):
  name=models.CharField(max_length=255)
  slug=models.SlugField(unique=True)
      
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
  name=models.CharField(max_length=30)
  category = models.ForeignKey(Category)
  image=models.ImageField('Article',upload_to= settings.MEDIA_ROOT)
  price=models.FloatField()
  notes=models.CharField(max_length=30,blank=True)
  created_on = models.DateTimeField(auto_now_add=True,editable=False)
  date_modified = models.DateTimeField(auto_now_add=True, editable=False)
  def serialize_fields(self):
    """Only these fields will be included in API responses."""
    return [
           'id',
            'name',
            'category',
            'image',
            'price',
            'notes',
            'created_on',
            'date_modified',
]

class Traded_article(models.Model):
  article = models.ForeignKey(Article)
  author = models.ForeignKey(User)
  created_on = models.DateTimeField(auto_now_add=True,editable=False)
  date_modified = models.DateTimeField(auto_now_add=True, editable=False)

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
