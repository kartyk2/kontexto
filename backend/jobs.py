from backend.config.database import client
from backend.config.constants import Constants
from backend.schemas import Game

database = client.get_database(Constants.DATABASE)
games_collection = database.get_collection(Constants.COLLECTION)


def pick_new_word():
    """ 
        picks a new word that the scheduler will add a new game in the database
        -- for now it only retuns a hardcoded word--
    """
    return "hello"


async def add_new_game():
    """
    make a new game and add it to the game table in DB
    """ 

    print("adding a new game to the game table")
    word = pick_new_word()
    _game = await games_collection.insert_one(
        Game(
            game= await games_collection.count_documents({}) + 1,
            target= word
        ).model_dump()
    )
    
    return _game.inserted_id



    