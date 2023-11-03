from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('report_lost_item', views.report_lost_item, name='report_lost_item'),    
    path('report_found_item', views.report_found_item, name='report_found_item'),
    path('afterReport', views.afterReport, name='afterReport'),
    path('searching', views.searching, name='searching')
]
