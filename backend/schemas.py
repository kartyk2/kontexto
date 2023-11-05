from pydantic import BaseModel

class Game(BaseModel):
    game: int
    target: str


class SuperUserCreds(BaseModel):
    username: str
    password: str