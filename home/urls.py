from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:tipoDeProduto>/<int:pk>/', views.detail, name='detail'),
    path('<str:tipoDeProduto>/', views.category, name='category'),
]