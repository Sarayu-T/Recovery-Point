from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from myapp import views

urlpatterns= [
    
    path('', views.initial_page,name='initial_page'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('signup_page', views.signup_page,name='signup_page'),
    path('login_page', views.login_page, name='login_page'),
    path('home', views.home, name='home'),
    path('report_lost_item', views.report_lost_item, name='report_lost_item'),    
    path('report_found_item', views.report_found_item, name='report_found_item'),
    path('afterReport', views.afterReport, name='afterReport'),
    path('view_reports', views.view_reports, name='view_reports'),
    path('ticket',views.ticket,name='ticket'),
    path('afterTicket', views.afterTicket, name='afterTicket'),     
    path('search/', views.search_items, name='search_items'),
    path('model_matching', views.model_matching, name='model_matching'),

    path('admin_user/', views.admin_user, name='admin_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'), 
    path('admin_ticket/', views.admin_ticket, name='admin_ticket'),     
    path('delete_ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('admin_lost_item/', views.admin_lost_item, name='admin_lost_item'),
    path('delete_lost_item/<int:id>/', views.delete_lost_item, name='delete_lost_item'),
    path('admin_found_item/', views.admin_found_item, name='admin_found_item'),
    path('delete_found_item/<int:id>/', views.delete_found_item, name='delete_found_item')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
