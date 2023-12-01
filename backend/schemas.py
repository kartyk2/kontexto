from pydantic import BaseModel

class Game(BaseModel):
    game_id: str
    target: str
    hints: dict[str, int]


class SuperUserCreds(BaseModel):
    username: str
    password: str