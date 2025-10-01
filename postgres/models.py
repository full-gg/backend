from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


default_test_statuses = [
    {"id": "0", "name": "Вклады", "status": "available"},
    {"id": "1", "name": 'Вклад "Плюсовой"', "status": "unavailable"},
    {"id": "2", "name": 'Вклад "Обгоняй"', "status": "unavailable"},
    {"id": "3", "name": "Кредиты", "status": "available"},
    {"id": "4", "name": "Ипотечный кредит", "status": "unavailable"},
    {"id": "5", "name": "Кредит наличными", "status": "unavailable"},
]


class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    health = Column(Integer, default=3)
    salary = Column(Integer, default=150_000)
    cash = Column(Integer, default=0)
    deposit = Column(Integer, default=0)
    tests_status = Column(JSON)
    avatar = Column(Integer, default=0)


class Tests(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    questions = Column(JSON, nullable=False)
    answers = Column(JSON, nullable=False)
    reward = Column(JSON, nullable=False)


class Global(Base):
    __tablename__ = "global"

    id = Column(Integer, primary_key=True, index=True)
    mortgage_rate = Column(Integer, nullable=False, default=15)
    mortgage_rate_min = Column(Integer, nullable=False, default=10)
    mortgage_rate_max = Column(Integer, nullable=False, default=20)
    target = Column(Integer, nullable=False, default=10_000_000)
    salary_addition = Column(Integer, nullable=False, default=10_000)


class DepositPlus(Base):
    __tablename__ = "plus"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    start_sum = Column(Integer)
    end_sum = Column(Integer)
    start_date = Column(Integer)
    end_date = Column(Integer)


class DepositOutrun(Base):
    __tablename__ = "outrun"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    start_sum = Column(Integer)
    end_sum = Column(Integer)
    start_date = Column(Integer)
    end_date = Column(Integer)

