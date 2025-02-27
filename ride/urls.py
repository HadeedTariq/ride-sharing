from django.urls import path
from . import views

app_name = "ride"

urlpatterns = [
    path("home/", views.homepage, name="home"),
    path("accept_driver/", views.acceptRide, name="accept_ride"),
    path("approve_ride/", views.approveRide, name="approve_ride"),
    path("cancel_ride/", views.cancelRide, name="cancel_ride"),
    path("driver/home/", views.driverpage, name="driver_home"),
]
