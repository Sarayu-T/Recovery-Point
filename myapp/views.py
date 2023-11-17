from django.shortcuts import render
from .models import LostItemDetails
import pymysql as sql

# Create your views here.
def searchbar(request):
  if request.method == 'GET':
    search = request.GET.get('search')
    post = LostItemDetails.objects.all().filter(title=search)
return render(request, 'searchbar.html', {'post': post})
