from django.urls import path
from . import views

urlpatterns = [
    path('transparency/', views.transparency_dashboard, name='transparency_dashboard'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
]