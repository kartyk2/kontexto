from backend.config.database import client
from backend.config.constants import Constants
from backend.schemas import Game
from backend.router.game_api import my_model
from gensim.models import Word2Vec
import traceback, random, datetime

common_word_model = Word2Vec.load("common_words.model")

database = client.get_database(Constants.DATABASE)
games_collection = database.get_collection(Constants.GAMES_COLLECTION)



def pick_new_word():
    """
    picks a new word that the scheduler will add a new game in the database
    -- for now it only retuns a hardcoded word --
    """
    vocab_size = common_word_model.wv.__len__()
    articles_and_prepositions = "a, an, the, about, above, across, after, against, along, amid, among, around, as, at, before, behind, below, beneath, beside, between, beyond, but, by, concerning, considering, despite, down, during, except, for, from, in, inside, into, like, near, next, off, on, onto, out, outside, over, past, regarding, round, since, through, throughout, till, to, toward, under, underneath, until, unto, up, upon, with, within, without"
    articles_and_prepositions = [word for word in articles_and_prepositions.split(sep= ", ")]

    while True:
        random_number = random.randint(0,1000000)
        index = random_number%vocab_size
        word= common_word_model.wv.index_to_key[index]
        if len(word) >= 3 and word not in articles_and_prepositions:
            return common_word_model.wv.index_to_key[index]


async def add_new_game():
    """
    make a new game and add it to the game table in DB
    """

    print("adding a new game to the game table")
    word = pick_new_word()

    similar_words = my_model.wv.similar_by_word(word, topn=Constants.MAX_HINTS)
    word_similarity_mapping = {
        similar_words[i][0]: i+1 for i in range(len(similar_words))
    }

    try:
        _game = await games_collection.insert_one(
            Game(
                game_id= datetime.datetime.now().strftime("%d%m%Y%H%M%S"),
                target=word,
                hints=word_similarity_mapping,
            ).model_dump()
        )
        print(_game, word)

    except Exception as error:
        print(traceback.format_exc())
