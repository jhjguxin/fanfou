from django.forms import ModelForm
from fanfou.apps.fanfou.models import Category,Article,Traded_article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['created_on','date_modified',]
class Traded_articleForm(ModelForm):
    class Meta:
        model = Traded_article
        exclude = ['author','article','total','pc','created_on']

