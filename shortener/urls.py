from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('api/link-stats/', views.link_stats, name="link_stats"),
    path('<str:code>/', views.redirect_url, name="redirect"),
]