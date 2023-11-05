from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import gensim
from typing import List
import traceback
from backend.config.database import client
from backend.config.constants import Constants

api_router = APIRouter()

my_model = gensim.models.Word2Vec.load('word2vec-amazon-cell-accessories-reviews-short.model')

database = Constants.DATABASE
collection = Constants.COLLECTION

game_collection = client.get_database(database).get_collection(collection)


@api_router.get("/similar", response_model=List[str])
async def get_similar(word: str):
    try:
        if word in my_model.wv:
            res = my_model.wv.most_similar(word, topn=10)
            similar_words = [item[0] for item in res]
            return similar_words
        else:
            raise HTTPException(status_code= 404, detail="i don't know this word")

    except Exception as error:
        raise HTTPException(500, detail= traceback.format_exception_only(error))
    

@api_router.get("/guess")
async def match_guess(word: str, game: int):
    try:
        word = word.lower()
        target_document = await game_collection.find_one(filter= {'game':game})
        game = target_document.get('game')
        target = target_document.get('target')
        if word in my_model.wv:
            res = my_model.wv.similarity(w1= word, w2 = target)
            return {"similarity": float(res)}
        else:
            raise HTTPException(status_code= 404, detail="i don't know this word")
    except Exception as error:
        return JSONResponse(status_code= 500, content= traceback.format_exception(error, limit= 1))


