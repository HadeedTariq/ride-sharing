from django.db import models

from authentication.models import User


# 2. Vehicle Model (For Drivers)
class Vehicle(models.Model):
    driver = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="driver_vehicle"
    )
    vehicle_type = models.CharField(
        max_length=20,
        choices=[("car", "Car"), ("bike", "Bike"), ("scooter", "Scooter")],
    )
    license_plate = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=20)


# 3. Ride Model
class Ride(models.Model):
    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("accepted", "Accepted"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    rider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rider_rides"
    )
    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="driver_rides",
    )
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="requested"
    )
    fare_estimate = models.DecimalField(max_digits=8, decimal_places=2)
    actual_fare = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# 4. Ride Requests Model
class RideRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
    ]
    rider = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    request_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")


# 6. Ratings & Reviews Model
class Rating(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    rider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rider_ratings"
    )
    driver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="driver_ratings"
    )
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


# 7. Ride Tracking Model
class RideTracking(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


# 9. Trip History Model
class TripHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


# 12. Ride Cancellations Model
class RideCancellation(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    canceled_by = models.CharField(
        max_length=10, choices=[("rider", "Rider"), ("driver", "Driver")]
    )
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


# 13. Driver Availability Model
class DriverAvailability(models.Model):
    driver = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[("online", "Online"), ("offline", "Offline"), ("busy", "Busy")],
    )
    last_updated = models.DateTimeField(auto_now=True)
