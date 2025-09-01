from django.urls import path
from . import views

urlpatterns = [
    path('montar_pc', views.pc_build, name='pc_build'),
]