"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from movies.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('movies.urls')),
    re_path(
        r'^assets/(?P<path>.*)$',
        serve,
        {'document_root': settings.ROOT_DIR / 'frontend' / 'dist' / 'assets'},
    ),
    re_path(r'^(?!api|admin).*$', index, name='index'),
]
