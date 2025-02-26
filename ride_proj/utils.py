import string
import random
import os
from dotenv import load_dotenv

import redis

load_dotenv()  # Load environment variables from .env

# Read Redis URL from environment variable
REDIS_URL = os.getenv("REDIS_HOST")


# Connect to Redis
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")


def generate_random_location(center_lat, center_lon, radius=0.01):
    return (
        center_lon + random.uniform(-radius, radius),  # Longitude
        center_lat + random.uniform(-radius, radius),  # Latitude
    )


def generate_random_string(length=8):
    # Combine letters and digits
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))
