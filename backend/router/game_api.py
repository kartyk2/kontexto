from fastapi import APIRouter, HTTPException
import gensim
from typing import List
import traceback

api_router = APIRouter()

my_model = gensim.models.Word2Vec.load('word2vec-amazon-cell-accessories-reviews-short.model')


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
    

@api_router.post("/guess")
async def match_guess(word: str):
    try:
        if word in my_model.wv:
            res = my_model.wv.similarity(w1= word, w2 = "hell")
            return {"similarity": float(res)}
        else:
            raise HTTPException(status_code= 404, detail="i don't know this word")
    except Exception as error:
        raise error.with_traceback()


