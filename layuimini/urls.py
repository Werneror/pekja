from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('api/clear/', views.api_clear, name='api_clear'),
    path('api/graph/', views.api_graph, name='api_graph'),
    path('page/dashboard/', views.dashboard, name='dashboard'),
    path('page/timeline/', views.timeline, name='timeline'),
    path('page/crontab/', views.crontab, name='crontab'),
]
