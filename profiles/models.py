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
