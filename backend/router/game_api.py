from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import gensim
from typing import List
import traceback, json, math
from backend.config.database import client
from backend.config.constants import Constants

api_router = APIRouter()

my_model = gensim.models.Word2Vec.load(
    "word2vec-amazon-cell-accessories-reviews-short.model"
)

database = Constants.DATABASE
collection = Constants.GAMES_COLLECTION

game_collection = client.get_database(database).get_collection(collection)

@api_router.get("/all_games")
async def get_All_games():
    async_cursor = game_collection.find({}, {"_id":0, "game_id":1})
    
    all_games = await async_cursor.to_list(None)
    return all_games


@api_router.get("/latest_game")
async def get_most_recent_game():
    most_recent_game = await game_collection.find_one({}, {"_id":0, "game_id":1}, sort=[("game_id", -1)])
    
    if most_recent_game:
        return most_recent_game
    else:
        return {"message": "No games found"}


@api_router.get("/similar", response_model=List[str])
async def get_similar(word: str):
    try:
        if word in my_model.wv:
            res = my_model.wv.most_similar(word, topn=10)
            similar_words = [item[0] for item in res]
            return similar_words
        else:
            raise HTTPException(status_code=404, detail="i don't know this word")

    except Exception as error:
        raise HTTPException(500, detail=traceback.format_exc())


@api_router.get("/guess")
async def match_guess(word: str, game_id: str):
    try:
        word = word.lower().strip()
        if word in my_model.wv:
            hints: dict = await game_collection.find_one(
                {"game_id": game_id},
                {"hints": 1, "_id": 0 } 
            )
            if hints:
                hints= hints.get(Constants.HINTS)
                rank = hints.get(word, 10001)
                return rank if rank != 0 else "WooooohhHH!!!!!!! You won..."

            else:
                return JSONResponse(status_code= 404, content= "OooppSss.... wrong game")
        
        else:
            return JSONResponse(status_code= 400, content= "Noo.. I  don't know this word")

    except Exception as error:
        return JSONResponse(
            status_code=500, content=traceback.format_exception(error, limit=1)
        )


@api_router.get("/hint")
async def get_hint(game_id: str, closest: int|None = None):
    """
    for game = game_id, return a hint when the user's best guess had closeness score of closest

    """
    hint_index = Constants.MAX_HINTS if not closest else math.ceil(closest*2/3)
    hints: dict = await game_collection.find_one(
        {"game_id": game_id},
        {"hints": 1, "_id": 0 } 
    )
    if hints:
        hints= hints.get(Constants.HINTS)
        for hint, rank in hints.items():
            if rank == hint_index:
                return hint
            
    else:
        return JSONResponse(status_code= 404, content= "OooppSss.... wrong game")
