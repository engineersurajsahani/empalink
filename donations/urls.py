from django.urls import path
from . import views

urlpatterns = [
    path('make-donation/<int:story_id>/', views.make_donation, name='make_donation'),
    path('admin/verification/', views.admin_donation_verification, name='admin_donation_verification'),
    path('admin/verify/<int:donation_id>/', views.verify_donation, name='verify_donation'),
    path('download-receipt/<int:donation_id>/', views.download_receipt, name='download_receipt'),
]