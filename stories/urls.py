from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_story, name='create_story'),
    path('my-stories/', views.my_stories, name='my_stories'),
    path('list/', views.story_list, name='story_list'),
    path('detail/<int:pk>/', views.story_detail, name='story_detail'),
    path('admin/approval/', views.admin_story_approval, name='admin_story_approval'),
    path('admin/approve/<int:pk>/', views.approve_story, name='approve_story'),
]