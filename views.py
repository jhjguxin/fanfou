# Create your views here.
from django.shortcuts import render_to_response,redirect
import pdb

def base_page(request):
  #pdb.set_trace()
  return render_to_response("base.html",)
def home(request):
  #pdb.set_trace()
  return render_to_response("index.html",{ 'user': request.user })
  #return redirect('/login')
