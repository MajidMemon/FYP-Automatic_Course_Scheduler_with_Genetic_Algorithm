
from django.contrib import admin
from django.urls import path, include # 👈 1. Add this line
from . import views

urlpatterns = [
    path('homelogin/', views.home_login, name='homelogin'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]