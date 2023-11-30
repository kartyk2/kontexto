from backend.config.database import client
from backend.config.constants import Constants
from backend.schemas import Game
from backend.router.game_api import my_model
import traceback

database = client.get_database(Constants.DATABASE)
games_collection = database.get_collection(Constants.GAMES_COLLECTION)


def pick_new_word():
    """
    picks a new word that the scheduler will add a new game in the database
    -- for now it only retuns a hardcoded word --
    """
    some = my_model.null_word
    print(some)
    
    return "hello"


async def add_new_game():
    """
    make a new game and add it to the game table in DB
    """

    print("adding a new game to the game table")
    word = pick_new_word()

    similar_words = my_model.wv.similar_by_word(word, topn=10000)
    word_similarity_mapping = {
        similar_words[i][0]: i for i in range(len(similar_words))
    }

    try:
        _game = await games_collection.insert_one(
            Game(
                game_id= await games_collection.count_documents({}) + 1,
                target=word,
                hints=word_similarity_mapping,
            ).model_dump()
        )
        print(_game)

    except Exception as error:
        print(traceback.format_exc())
