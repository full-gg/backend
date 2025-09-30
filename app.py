from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from postgres.client import Session
from postgres.models import User, Global, Tests
import random

app = Flask(__name__)


test_dependencies = {0: [1, 2], 3: [4, 5]}


def action(user_id):
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if user.health == 0:
            return Response("No health available", status=400)
        user.health -= 1
        session.commit()


@app.route('/auth', methods=["POST"])
def auth():
    data = request.get_json()
    user_id = data["user_id"]
    with Session() as session:
        if session.get(User, user_id) is None:
            session.add(
                User(
                    id=user_id,
                    health=3,
                    salary=150_000,
                    cash=150_000,
                    deposit=0,
                    tests_status=[
                        {"id": "0", "name": "Вклады", "status": "available"},
                        {"id": "1", "name": 'Вклад "Плюсовой"', "status": "unavailable"},
                        {"id": "2", "name": 'Вклад "Обгоняй"', "status": "unavailable"},
                        {"id": "3", "name": "Кредиты", "status": "available"},
                        {"id": "4", "name": "Ипотечный кредит", "status": "unavailable"},
                        {"id": "5", "name": "Кредит наличными", "status": "unavailable"},
                    ]
                )
            )
            session.commit()
            return Response(status=201)
    return Response(status=200)


@app.route('/mortgage_rate')
def get_mortgage_rate():
    with Session() as session:
        result = session.get(Global, 0).mortgage_rate
        return jsonify(result)


@app.route('/hp', methods=["GET"])
def get_health():
    user_id = request.args.get("user_id")
    with Session() as session:
        result = session.get(User, user_id).health
        return jsonify(result)


@app.route('/salary', methods=["GET"])
def get_salary():
    user_id = request.args.get("user_id")
    with Session() as session:
        result = session.get(User, user_id).salary
        return jsonify(result)


@app.route('/name', methods=["GET"])
def get_name():
    user_id = request.args.get("user_id")
    with Session() as session:
        result = session.get(User, user_id).user_id
        return jsonify(result)


@app.route('/lectures', methods=["GET"])
def get_lectures():
    user_id = request.args.get("user_id")
    action(user_id)
    with Session() as session:
        lectures = session.get(User, user_id).tests_status
        return jsonify(lectures)


@app.route('/test', methods=["GET"])
def get_test():
    user_id = request.args.get("user_id")
    test_id = request.args.get("test_id")
    action(user_id)
    with Session() as session:
        questions = session.get(Tests, test_id).questions
        return jsonify(questions)


@app.route('/answer', methods=["POST"])
def post_answer():
    data = request.get_json()
    user_id = data["user_id"]
    test_id = data["id"]
    answers = data["answers"]
    with Session() as session:
        correct_answers = session.get(Tests, test_id).answers
        matching_answers = 0
        for i in range(len(answers)):
            if answers[i] == correct_answers[i]:
                matching_answers += 1
        reward = session.get(Tests, test_id).reward[matching_answers]
        old_salary = session.get(User, user_id).salary
        if reward == 0:
            return jsonify({"correct_answers": f"{matching_answers}/{len(answers)}", "salary_addition": "0", "new_salary": old_salary})
        salary_addition = session.get(Global, 0).salary_addition * reward
        user = session.query(User).filter_by(id=user_id).first()
        new_salary = user.salary + salary_addition
        user.salary = new_salary
        if test_id in test_dependencies:
            for i in test_dependencies[test_id]:
                user.tests_status[i]["status"] = "available"
        session.commit()
        return jsonify({"correct_answers": f"{matching_answers}/{len(answers)}", "salary_addition": "salary_addition", "new_salary": new_salary})
