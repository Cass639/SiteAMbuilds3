from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:tipo_slug>/<int:pk>/', views.detail, name='detail'),
    path('<str:tipo_slug>/', views.category, name='category'),
]