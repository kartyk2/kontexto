from fastapi import FastAPI, HTTPException
import gensim
from typing import List


app = FastAPI()

my_model = gensim.models.Word2Vec.load('word2vec-amazon-cell-accessories-reviews-short.model')

@app.get("/")
async def root():
    return ("Hello Welcome to knotexto")

@app.get("/similar", response_model=List[str])
async def get_similar(word: str):
    if word in my_model.wv:
        res = my_model.wv.most_similar(word, topn=10)
        similar_words = [item[0] for item in res]
        return similar_words
    else:
        raise HTTPException(status_code= 404, detail="i don't know this word")


@app.post("/guess")
async def match_guess(word: str):
    try:
        if word in my_model.wv:
            res = my_model.wv.similarity(w1= word, w2 = "hell")
            return {"similarity": float(res)}
        else:
            raise HTTPException(status_code= 404, detail="i don't know this word")
    except Exception as error:
        raise error

