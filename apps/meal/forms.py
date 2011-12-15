from django.forms import ModelForm
from fanfou.apps.meal.models import Order,Restaurant

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ['user','date','pc','total']
class RestaurantForm(ModelForm):
    class Meta:
        model = Order

