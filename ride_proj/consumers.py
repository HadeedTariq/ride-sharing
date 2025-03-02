# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


from ride_proj.utils import generate_random_location, redis_client

USER_LAT = 31.5490304
USER_LON = 74.4062976


class DriverConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_id = self.scope["url_route"]["kwargs"]["driver_id"]
        self.room_group_name = f"driver_{self.driver_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

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
        if task_type == "driver_location":
            driver_id = self.driver_id
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
                return
            redis_client.geoadd("drivers", (longitude, latitude, f"driver_{driver_id}"))

            await self.send(
                text_data=json.dumps(
                    {
                        "message": "Location updated",
                    }
                )
            )
        if task_type == "update_location":
            driver_id = self.driver_id
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            customer_id = data.get("customer_id")

            if not driver_id and not latitude and not longitude:
                await self.send(
                    text_data=json.dumps(
                        {
                            "message": "All the parameters are required",
                        }
                    )
                )
                return
            self.customer_group = f"customer_{customer_id}"
            await self.channel_layer.group_send(
                self.customer_group,
                {
                    "type": "broadcast_location",
                    "task_type": "broadcast_location",
                    "latitude": latitude,
                    "longitude": longitude,
                },
            )

    async def ride_approval(self, event):
        """Handles the ride approval message sent from the Django view"""
        message = event["message"]
        customer_id = event["customer_id"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "type": "ride_approval",
                    "customer_id": customer_id,
                }
            )
        )


class CustomerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.customer_id = self.scope["url_route"]["kwargs"]["customer_id"]
        self.customer_group = f"customer_{self.customer_id}"
        await self.channel_layer.group_add(self.customer_group, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.customer_group, self.channel_name)

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

    async def broadcast_location(self, event):
        """Receive location update from driver and send to customer"""
        await self.send(text_data=json.dumps(event))
