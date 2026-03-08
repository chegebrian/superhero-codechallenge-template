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

# heroes route
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

# specific hero
@app.route("/heroes/<int:id>")
def get_hero(id):

    hero = Hero.query.get(id)

    if not hero:
        return {"error": "Hero not found"}, 404

    return jsonify(hero.to_dict()), 200

# powers route
@app.route("/powers")
def get_powers():
    powers = Power.query.all()
    powers_list = [power.to_dict(only=("id", "name", "description")) for power in powers]
    return jsonify(powers_list), 200

# specific power route
@app.route("/powers/<int:id>")
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict(only=("id", "name", "description"))), 200

# edit hero power
@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):

    power = Power.query.get(id)

    if not power:
        return {"error": "Power not found"}, 404

    data = request.get_json()

    try:
        power.description = data["description"]

        db.session.commit()

        return jsonify(power.to_dict()), 200

    except ValueError as e:

        return {"errors": [str(e)]}, 400

# add a hero power 
@app.route("/hero_powers", methods=["POST"])
def create_hero_power():

    data = request.get_json()

    try:

        hero_power = HeroPower(
            strength=data["strength"],
            hero_id=data["hero_id"],
            power_id=data["power_id"]
        )

        db.session.add(hero_power)
        db.session.commit()

        return jsonify(hero_power.to_dict()), 201

    except ValueError as e:

        return {"errors": [str(e)]}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
