from pydantic import BaseModel

class Game(BaseModel):
    game: int
    target: str
