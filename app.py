from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    lastname = db.Column(db.String(100), unique=False)
    house = db.Column(db.String(20), unique=False)
    pic = db.Column(db.String(200), unique=False)
    bloodStatus = db.Column(db.String(100), unique=False)
    wand = db.Column(db.String(200), unique=False)
    patronus = db.Column(db.String(200), unique=False)

    def __init__(self, name, lastname, house, pic, bloodStatus, wand, patronus):
        self.name = name
        self.lastname = lastname
        self.house = house
        self.pic = pic
        self.bloodStatus = bloodStatus
        self.wand = wand
        self.patronus = patronus


class CharacterSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'lastname', 'house', 'pic', 'bloodStatus', 'wand', 'patronus')


character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)

# Endpoint to create a new character
@app.route('/character', methods=["POST"])
def add_character():
    name = request.json['name']
    lastname = request.json['lastname']
    house = request.json['house']
    pic = request.json['pic']
    bloodStatus = request.json['bloodStatus']
    wand = request.json['wand']
    patronus = request.json['patronus']


    new_character = Character(name, lastname, house, pic, bloodStatus, wand, patronus)

    db.session.add(new_character)
    db.session.commit()

    character = Character.query.get(new_character.id)

    return character_schema.jsonify(character)

# Endpoint to query all characters
@app.route("/characters", methods=["GET"])
def get_characters():
    all_characters = Character.query.all()
    result = characters_schema.dump(all_characters)
    return jsonify(result)

# Endpoint for querying a single character
@app.route("/character/<id>", methods=["GET"])
def get_character(id):
    character = Character.query.get(id)
    return character_schema.jsonify(character)

# Endpoint for updating a character
@app.route("/character/<id>", methods=["PUT"])
def character_update(id):
    character = Character.query.get(id)
    name = request.json['name']
    lastname = request.json['lastname']
    house = request.json['house']
    pic = request.json['pic']
    bloodStatus = request.json['bloodStatus']
    wand = request.json['wand']
    patronus = request.json['patronus']

    character.name = name
    character.lastname = lastname
    character.house = house
    character.pic = pic
    character.bloodStatus = bloodStatus
    character.wand = wand
    character.patronus = patronus

    db.session.commit()
    return character_schema.jsonify(character)

# Endpoint for deleting a character
@app.route("/character/<id>", methods=["DELETE"])
def character_delete(id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    return "Character was successfully deleted"

if __name__ == '__main__':
    app.run(debug=True)