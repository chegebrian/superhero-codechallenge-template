#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from server.models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route("/heroes")
def get_heroes():

    heroes = Hero.query.all()

    heroes_list = [
        {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        for hero in heroes
    ]

    return jsonify(heroes_list), 200

@app.route("/heroes/<int:id>")
def get_hero(id):

    hero = Hero.query.get(id)

    if not hero:
        return {"error": "Hero not found"}, 404

    return jsonify(hero.to_dict()), 200

@app.route("/powers")
def get_powers():

    powers = Power.query.all()

    return jsonify([p.to_dict() for p in powers]), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
