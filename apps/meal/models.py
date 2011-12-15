from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import datetime
class Restaurant((models.Model)):
    article=models.CharField(max_length=30,default='default_article')
    img=models.ImageField('Image',upload_to= 'restaurant')
    notes=models.TextField(help_text=_(u'write your preferences.'))
    hoter=models.IntegerField(blank=True,default=0)
    date = models.DateField(default=datetime.date.today)  # no parens on 'today', this is on purpose

    @models.permalink
    def get_absolute_url(self):
        return('restaurant_detail', (), {
                    'year': self.date.strftime("%Y"),
                    'month': self.date.strftime("%m").lower(),
                    'day': self.date.strftime("%d"),
                    'id': self.id })
    def __unicode__(self):
        return self.article


class Order(models.Model):
    date = models.DateField(default=datetime.date.today)  # no parens on 'today', this is on purpose
    ##username = models.CharField(max_length=64,editable=False)
    user = models.ForeignKey(User)
    #guests = models.IntegerField(default=0)
    guests = models.IntegerField(default=0)
    article=models.CharField(max_length=30,help_text=_(u'write you want.'))
    restaurant=models.ForeignKey(Restaurant,help_text=_(u'Make sure you choose the righ restaurant.'))
    price = models.IntegerField(default=0,help_text=_(u'please input the price.'))
    total = models.IntegerField(default=0)
    notes=models.CharField(max_length=30,blank=True)
    pc=models.CharField(max_length=30)

    def __str__(self):
        return '%s on %s with %s guests' % (self.user.username, self.date, self.guests)

    def __repr__(self):
        return '%s on %s with %s guests' % (self.user.username, self.date, self.guests)

