from django.urls import path
from myapp import views

app_name='myapp'
urlpatterns = [
    path('search/', views.search, name='search'),    
]
