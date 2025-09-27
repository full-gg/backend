from flask import Flask, request, jsonify
import random

app = Flask(__name__)


@app.route('/mortgage_rate')
def get_mortgage_rate():
    return jsonify({"value": "20"})


@app.route('/hp_update')
def get_health():
    health = random.randint(1, 5)
    return jsonify({"value": f"{health}"})
