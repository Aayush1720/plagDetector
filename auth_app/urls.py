from django.contrib import admin
from django.urls import path, include
from django.urls.resolvers import URLPattern
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('logout', views.logout, name="logout"),
]