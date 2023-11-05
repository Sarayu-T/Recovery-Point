from django.urls import path
from myapp import views

urlpatterns= [
    path('',views.home,name='home'),
    path('ticket/',views.ticket,name='ticket'),
    path('afterTicket/', views.afterTicket, name='afterTicket'),
    path('afterReport/',views.afterReport, name='afterReport')
]