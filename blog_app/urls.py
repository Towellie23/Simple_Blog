from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_listing, name='home'),
    path('register', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post_create/', views.post_create, name='post_create'),
    path('post_edit/<int:id>/', views.post_edit, name='post_edit'),
    path('post_delete/<int:id>/', views.post_delete, name='post_delete'),
]
