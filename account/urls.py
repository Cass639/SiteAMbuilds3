from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("password_reset", views.password_reset, name="password_reset"),  # New path for password reset
]
