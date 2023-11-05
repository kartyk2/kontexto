from fastapi import FastAPI
from backend.router.game_api import api_router
from backend.scheduler import sched

app = FastAPI()

app.include_router(api_router)


@app.get("/")
async def root():
    return "Hello, Welcome to kontexto"
 
@app.on_event('startup')
def startup_chores():
    print("getting started")
    sched.start()


@app.on_event('shutdown')
def startup_chores():
    print("shutting_down")
    sched.shutdown()

