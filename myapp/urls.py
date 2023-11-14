from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup_page/', views.signup_page,name='signup_page'),
    path('login_page/', views.login_page, name='login_page'),
]