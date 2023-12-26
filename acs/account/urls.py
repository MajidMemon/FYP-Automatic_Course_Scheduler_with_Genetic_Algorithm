from django.urls import path, include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path('', include('django.contrib.auth.urls')),
    #path('', views.loginpage, name='loginpage'),
    path('homelogin/', views.home_login, name='homelogin'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]