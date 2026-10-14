from django.urls import path
from . import views

urlpatterns = [
    path('health', views.api_health, name='api_health'),
    path('movies', views.api_movies, name='api_movies'),
    path('filter-options', views.api_filter_options, name='api_filter_options'),
    path('search', views.api_search, name='api_search'),
    path('filter', views.api_filter, name='api_filter'),
]
