from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import dotenv_values

#place the .env files in the same dir as main

creds = dotenv_values(".env")
client = AsyncIOMotorClient(creds.get("DB_CONNECTION"))

DATABASE = creds.get("DB_NAME")
GAMES = "games"


# db = client.get_database(DATABASE)
# games_collection = db.get_collection(GAMES)

# async def get_game():
#     game = await games_collection.find()
#     return game

# game = get_game()
# print(game , type(game))

# import asyncio
# from motor.motor_asyncio import AsyncIOMotorClient

# Assuming you have defined DATABASE and GAMES variables

# async def get_game():
#     # with AsyncIOMotorClient() as client:
#     db = client.get_database(DATABASE)
#     games_collection = db.get_collection(GAMES)
#     game = games_collection.find()  # Modify the query as per your needs
#     return game

# async def main():
#     games = await get_game()
#     async for game in games:
#         print(game, type(game))

# # Run the asynchronous function within an event loop
# if __name__ == "__main__":
#     asyncio.run(main())


