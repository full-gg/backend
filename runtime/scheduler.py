import random

from flask_apscheduler import APScheduler
from postgres.client import Session
from postgres.models import User, Global, Tests, default_test_statuses


scheduler = APScheduler()


@scheduler.task('cron', id='heal', hour='*/8')
def heal():
    with Session() as session:
        users = session.query(User).all()
        for user in filter(lambda u: u.health < 3, users):
            user.health += 1
        session.commit()


@scheduler.task('cron', id='salary', minute=0, hour=0, day='*/4')
def salary():
    with Session() as session:
        users = session.query(User).all()
        for user in users:
            user.cash += user.salary
        session.commit()


@scheduler.task('cron', id='mortgage_rate', minute=0, hour=0, day='*/4')
def mortgage_rate():
    with Session() as session:
        global_values = session.query(Global).filter_by(id=0).first()
        global_values.mortgage_rate = random.randint(global_values.mortgage_rate_min, global_values.mortgage_rate_max)
        session.commit()
