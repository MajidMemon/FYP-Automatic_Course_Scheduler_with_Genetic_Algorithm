# urls.py

from django.urls import path
from .views import run_genetic_algorithm

urlpatterns = [
    # ... other URL patterns
    path('', run_genetic_algorithm, name='run_genetic_algorithm'),
]