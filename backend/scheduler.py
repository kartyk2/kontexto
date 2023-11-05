from apscheduler.schedulers.background import BackgroundScheduler
from backend.jobs import add_new_game

sched= BackgroundScheduler()

sched.add_job(add_new_game, trigger= 'interval', minutes= 3)


