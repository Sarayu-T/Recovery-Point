from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.signup_page,name='signup_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('home', views.home, name='home'),
    path('report_lost_item', views.report_lost_item, name='report_lost_item'),    
    path('report_found_item', views.report_found_item, name='report_found_item'),
    path('afterReport', views.afterReport, name='afterReport'),

]
