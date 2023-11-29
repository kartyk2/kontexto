from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import dotenv_values

#place the .env files in the same dir as main

creds = dotenv_values(".env")

cloud_uri = creds.get("CLOUD_URI")
client = AsyncIOMotorClient(creds.get("CLOUD_URI"))

DATABASE = creds.get("DB_NAME")
GAMES = "games"

class ConnectionManager:
    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(cloud_uri)

    def __enter__(self):
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
