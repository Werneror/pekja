from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('api/clear/', views.api_clear, name='api_clear'),
    path('api/graph/', views.api_graph, name='api_graph'),
    path('api/input_file/', views.api_input_file, name='api_input_file'),
    path('api/output_file/', views.api_output_file, name='api_output_file'),
    path('download/<str:file_name>', views.download, name='daownload'),
    path('page/dashboard/', views.dashboard, name='dashboard'),
    path('page/timeline/', views.timeline, name='timeline'),
    path('page/crontab/', views.crontab, name='crontab'),
    path('page/email_report/', views.email_report, name='email_report'),
    path('page/input/', views.input_file, name='input_file'),
    path('page/output/', views.output_file, name='output_file'),
]
