# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


from ride_proj.utils import generate_random_location, redis_client

USER_LAT = 31.5490304
USER_LON = 74.4062976


class DriverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        headers = dict(self.scope["headers"])

        cookie_header = headers.get(b"cookie", b"").decode("utf-8")

        # Parse the cookie string into a dictionary
        cookies = {}
        if cookie_header:
            for cookie in cookie_header.split("; "):
                key, value = cookie.split("=", 1)
                cookies[key] = value

        # Now you can use the cookies
        sessionid = cookies.get("access_token")
        print(f"Session ID: {sessionid}")

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):

        data = json.loads(text_data)
        task_type = data.get("task_type")
        if task_type == "general":

            await self.send(
                text_data=json.dumps(
                    {
                        "message": "Hello from the server",
                    }
                )
            )
            return
        driver_id = data.get("driver_id")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not driver_id and not latitude and not longitude:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": "All the parameters are required",
                    }
                )
            )

        # Add driver location to Redis
        redis_client.geoadd("drivers", (longitude, latitude, driver_id))

        await self.send(
            text_data=json.dumps(
                {
                    "message": "Location updated",
                }
            )
        )
