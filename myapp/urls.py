from django.urls import path
from myapp import views

urlpatterns = [
    path('searchbar/', views.searchbar, name='searchbar'),    
]
