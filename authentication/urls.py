from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("register/", views.registerUser, name="registerUser"),
    path("login/", views.loginUser, name="loginUser"),
]
