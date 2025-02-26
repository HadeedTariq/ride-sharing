from datetime import datetime
import json
import os
from django.http import JsonResponse
from django.shortcuts import render
import logging
from .utils import estimate_fare
from ride_proj.utils import redis_client
from geopy.distance import geodesic


from authentication.models import User


from .models import Ride, RideRequest

logger = logging.getLogger(__name__)

open_cage_api_key = os.getenv("OPEN_CAGE_API_KEY")


def homepage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        currentLocation = data.get("currentLocation")
        currentLat = currentLocation.split("----")[0]
        currentLon = currentLocation.split("----")[1]
        pickup = data.get("pickup")
        dropoff = data.get("dropoff")

        ride_request = RideRequest.objects.create(
            rider_id=request.user_data["id"],
            pickup_location=pickup,
            dropoff_location=dropoff,
        )

        nearby_drivers = redis_client.georadius(
            "drivers",
            currentLon,
            currentLat,
            10,
            unit="km",
        )

        return JsonResponse(
            {
                "nearby_drivers": nearby_drivers,
                "ride_id": ride_request.id,
            },
            status=200,
        )

    context = {
        "tile_url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "subdomains": ["a", "b", "c"],
        "zoom_level": 12,
        "latitude": 31.5204,
        "longitude": 74.3587,
        "map_attribution": "&copy; OpenStreetMap contributors",
        "apiKey": open_cage_api_key,
    }

    return render(request, "ride/index.html", context)


def acceptRide(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        rider_id = request.user_data.get("id")

        data = json.loads(request.body)

        driver = data.get("driver_name")
        ride_id = data.get("ride_id")
        current_location = data.get("currentLocation")
        destination_location = data.get("destinationLocation")

        # Validate required fields
        if not all([driver, ride_id, current_location, destination_location]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Extract driver ID safely
        try:
            driver_id = int(driver.split("_")[1])
        except (IndexError, ValueError):
            return JsonResponse({"error": "Invalid driver format"}, status=400)

        # Extract and validate latitude & longitude
        try:
            pickup_lat, pickup_lon = map(float, current_location.split("----"))
            drop_lat, drop_lon = map(float, destination_location.split("----"))
        except (ValueError, IndexError):
            return JsonResponse({"error": "Invalid location format"}, status=400)

        # Fetch ride request
        try:
            ride_request = RideRequest.objects.get(id=ride_id)
        except RideRequest.DoesNotExist:
            return JsonResponse({"error": "Ride request not found"}, status=404)

        # Update ride request status
        ride_request.status = "accepted"
        ride_request.save()

        # Calculate distance and estimated fare
        distance_km = geodesic(
            (pickup_lat, pickup_lon), (drop_lat, drop_lon)
        ).kilometers
        estimated_fare = estimate_fare(distance_km)

        # Create new ride entry
        ride_data = Ride.objects.create(
            rider_id=rider_id,
            driver_id=driver_id,
            pickup_location=ride_request.pickup_location,
            dropoff_location=ride_request.dropoff_location,
            fare_estimate=estimated_fare,
        )

        return JsonResponse(
            {
                "message": "Ride accepted successfully",
                "estimated_fare": estimated_fare,
                "ride_id": ride_data.id,
            },
            status=200,
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({"error": "Something went wrong"}, status=500)


def approveRide(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        logger.info(data)
        ride_id = data.get("ride_id")

        if not ride_id:
            return JsonResponse({"error": "Missing ride_id"}, status=400)

        # Fetch ride request safely
        ride_request = RideRequest.objects.filter(id=ride_id).first()
        if not ride_request:
            return JsonResponse({"error": "Ride request not found"}, status=404)

        # Update ride request status
        ride_request.status = "accepted"
        ride_request.save()
        print(ride_request.id)
        return JsonResponse(
            {"message": "Ride approved successfully", "ride_id": ride_request.id},
            status=200,
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        logger.error(f"Unexpected error in approveRide: {str(e)}", exc_info=True)
        return JsonResponse({"error": "Something went wrong"}, status=500)


def driverpage(request):
    users = User.objects.values("id", "email")  # Specify the fields you need.
    print(list(users))
    context = {
        "tile_url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "subdomains": ["a", "b", "c"],
        "zoom_level": 16,
        "latitude": 31.5204,
        "longitude": 74.3587,
        "map_attribution": "&copy; OpenStreetMap contributors",
        "apiKey": open_cage_api_key,
    }
    return render(request, "ride/driver.html", context)
