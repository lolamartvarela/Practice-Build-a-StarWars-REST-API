"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Favoritos, Personajes, Planetas, Vehiculos
#from models import Person

# Importacion JWT
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)
app.url_map.strict_slashes = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET USUARIO
@app.route('/usuario', methods=['GET'])
def handle_usuario():
    allusuario = Usuario.query.all()
    results = list(map(lambda item: item.serialize(),allusuario))

    return jsonify(results), 200

# GET USUARIO FAVORITOS
@app.route('/usuario/<int:usuario_id>/favoritos/', methods=['GET'])
def get_favoritos_usuario(usuario_id):
    
    usuario_favoritos = Favoritos.query.filter_by(usuario_id=usuario_id).all()
    results = list(map(lambda item: item.serialize(),usuario_favoritos))
    print(results)
    return jsonify(results), 200

# GET TODOS PERSONAJES
@app.route('/personajes', methods=['GET'])
def handle_personajes():
    allpersonajes = Personajes.query.all()
    results = list(map(lambda item: item.serialize(),allpersonajes))

    return jsonify(results), 200

# GET PERSONAJES 
@app.route('/personajes/<int:personajes_id>', methods=['GET'])
def get_info_personajes(personajes_id):
    
    user = Personajes.query.filter_by(id=personajes_id).first()
    return jsonify(personajes.serialize()), 200


# GET TODOS PLANETAS
@app.route('/planetas', methods=['GET'])
def handle_planetas():
    allplanetas = Planetas.query.all()
    results = list(map(lambda item: item.serialize(),allplanetas))

    return jsonify(results), 200

# GET PLANETAS
@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def get_info_planetas(planetas_id):
    
    user = Planetas.query.filter_by(id=planetas_id).first()
    return jsonify(planetas.serialize()), 200

# POST PLANETAS
@app.route('/usuario/<int:usuario_id>/favoritos/planetas', methods=['POST'])
def add_new_favourite_planet(usuario_id):
    request_body = request.json
    print(request_body)
    print(usuario_id)
    new_favorito = Favoritos(usuario_id=usuario_id, planetas_id=request_body["planetas_id"])
    db.session.add(new_favorito)
    db.session.commit()
    usuario = Favoritos.query.filter_by(usuario_id=usuario_id).first()
    print(usuario)
    return jsonify(request_body),200

# POST PERSONAJES
@app.route('/usuario/<int:usuario_id>/favoritos/personajes', methods=['POST'])
def add_new_favourite_person(usuario_id):
    request_body = request.json
    print(request_body)
    print(usuario_id)
    new_favorito = Favoritos(usuario_id=usuario_id, personajes_id=request_body["personajes_id"])
    db.session.add(new_favorito)
    db.session.commit()
    usuario = Favoritos.query.filter_by(usuario_id=usuario_id).first()
    print(usuario)
    return jsonify(request_body),200

    # DELETE PLANETAS
@app.route('/usuario/<int:usuario_id>/favoritos/planetas', methods=['DELETE'])
def eliminar_planeta_favorito(usuario_id):
    request_body=request.json
    print(request_body)
    print(usuario_id)
    query= Favoritos.query.filter_by(usuario_id=usuario_id,planetas_id=request_body["planetas_id"]).first()
    print(query)
    if query is None:
        return jsonify({"msg":"No hubo coincidencias, no hay nada para eliminar"}),404
    db.session.delete(query)
    db.session.commit() 
    return jsonify({"msg":"El favorito ha sido eliminado correctamente"}),200

        # DELETE PERSONAJES
@app.route('/usuario/<int:usuario_id>/favoritos/personajes', methods=['DELETE'])
def eliminar_personaje_favorito(usuario_id):
    request_body=request.json
    print(request_body)
    print(usuario_id)
    query= Favoritos.query.filter_by(usuario_id=usuario_id,personajes_id=request_body["personajes_id"]).first()
    print(query)
    if query is None:
        return jsonify({"msg":"No hubo coincidencias, no hay nada para eliminar"}),404
    db.session.delete(query)
    db.session.commit() 
    return jsonify({"msg":"El favorito ha sido eliminado correctamente"}),200

# @app.route('/user', methods=['POST'])
# def add_user():
#     request_body = request.data
#     decoded_object = json.loads(request_body)
#     get_email = User.query.filter_by(email=decoded_object["email"]).first()
#     if get_email is None:
#         new_user = User(user_name=decoded_object["user_name"], email=decoded_object["email"], password=decoded_object["password"])
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({"msg":"usuario creado exitosamente"}), 200
#     else:
#         return jsonify({"msg":"el email ya existe"}), 400

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    get_usuario = Usuario.query.filter_by(email=email).first()
    print(get_usuario.email)
   
    if email != get_usuario.email or password != get_usuario.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_usuario = get_jwt_identity()
    get_usuario = Usuario.query.filter_by(email=current_usuario).first()
    print(get_usuario.serialize())
    return jsonify(logged_in_as=current_usuario), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
