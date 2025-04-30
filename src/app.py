import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, FavoritePlanet, FavoritePeople

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    user = User.query.get(1)
    return jsonify({
        "msg": "GET / People for this project",
        "user": user.serialize()
    }), 200

# PLANETS
@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    return jsonify({
        "msg": "GET / Planets for this project",
        "planets": [planet.serialize() for planet in planets]
    }), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        raise APIException('Planet not found', status_code=404)
    return jsonify({
        "msg": "GET / Solo 1 planeta",
        "Planet": planet.serialize()
    }), 200

@app.route('/planet', methods=['POST'])
def post_planet():
    data = request.get_json()
    if not data or 'name' not in data or data['name'] == "":
        raise APIException('El campo "name" es requerido', status_code=400)
    new_planet = Planet(
        name=data["name"],
        rotation_period=data["rotation_period"],
        orbital_period=data["orbital_period"],
        diameter=data["diameter"],
        climate=data["climate"],
        terrain=data["terrain"],
        population=data["population"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({
        "msg": f"El nuevo planeta creado es: {new_planet.name}",
        "new_planet": new_planet.serialize()
    }), 201

# PEOPLE
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify({"People": [person.serialize() for person in people]}), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        raise APIException('Person not found', status_code=404)
    return jsonify({
        "msg": "GET / Solo 1 persona",
        "user": person.serialize()
    }), 200

@app.route('/people', methods=['POST'])
def post_people():
    data = request.get_json()
    if not data or 'name' not in data or data['name'] == "" or data.get("planet_id") == "":
        raise APIException('Campos requeridos faltantes', status_code=400)
    new_person = People(
        name=data["name"],
        height=data["height"],
        hair_color=data["hair_color"],
        skin_color=data["skin_color"],
        eye_color=data["eye_color"],
        birth_year=data["birth_year"],
        gender=data["gender"],
        planet_id=data["planet_id"]
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({
        "msg": f"El nuevo personaje creado es: {new_person.name}",
        "new_person": new_person.serialize()
    }), 201

# FAVORITES - PLANETS
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(planet_id):
    data = request.get_json()
    if not data or 'user_id' not in data:
        raise APIException('El campo "user_id" es requerido', status_code=400)

    existing = FavoritePlanet.query.filter_by(user_id=data["user_id"], planet_id=planet_id).first()
    if existing:
        return jsonify({"msg": "Este planeta ya está en favoritos"}), 200

    new_favorite = FavoritePlanet(user_id=data["user_id"], planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({
        "msg": "Planeta favorito agregado",
        "favorite": new_favorite.serialize()
    }), 201

@app.route('/favorite/planet/<int:user_id>', methods=['GET'])
def get_favorite_planet(user_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('Usuario no encontrado', status_code=404)

    favorites = FavoritePlanet.query.filter_by(user_id=user_id).all()
    return jsonify({
        "msg": "Here is all your favorite Planets, enjoy",
        "Favorite_planet": [f.serialize() for f in favorites]
    }), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1  # Hardcoded, puedes adaptar esto
    favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "No se encontró ese favorito"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Planeta eliminado de favoritos"}), 200

# FAVORITES - PEOPLE
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people(people_id):
    data = request.get_json()
    if not data or 'user_id' not in data:
        raise APIException('El campo "user_id" es requerido', status_code=400)

    existing = FavoritePeople.query.filter_by(user_id=data["user_id"], people_id=people_id).first()
    if existing:
        return jsonify({"msg": "Este personaje ya está en favoritos"}), 200

    new_favorite = FavoritePeople(user_id=data["user_id"], people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({
        "msg": "Personaje favorito agregado",
        "favorite": new_favorite.serialize()
    }), 201

@app.route('/favorite/people/<int:user_id>', methods=['GET'])
def get_favorite_people(user_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('Usuario no encontrado', status_code=404)

    favorites = FavoritePeople.query.filter_by(user_id=user_id).all()
    return jsonify({
        "msg": "Here is all your favorite People, enjoy",
        "Favorite_people": [f.serialize() for f in favorites]
    }), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1  # Hardcoded
    favorite = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "No se encontró ese favorito"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Personaje eliminado de favoritos"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
