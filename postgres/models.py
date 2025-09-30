from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    health = Column(Integer)
    salary = Column(Integer)
    cash = Column(Integer)
    deposit = Column(Integer)
    tests_status = Column(JSON)


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

