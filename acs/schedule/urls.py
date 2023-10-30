from django.contrib import admin
from django.urls import path , include
from schedule import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('product', views.product, name='product'),
    path('resource', views.resource, name='resource'),
    path('pricing', views.pricing, name='pricing')

]
