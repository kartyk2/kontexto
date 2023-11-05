from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.jobs import add_new_game

sched= AsyncIOScheduler()

sched.add_job(add_new_game, trigger= 'interval', minutes= 10)