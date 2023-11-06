from django.shortcuts import render
from .models import Item
import pymysql as sql

# Create your views here.
def search(request):
  query = request.GET.get('search')
  results = Item.objects.filter(item_name__icontains=query) | Item.objects.filter(location_lost__icontains=query)

return render(request, 'searching.html')
