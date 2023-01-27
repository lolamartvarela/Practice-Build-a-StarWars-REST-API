from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # usuario_id = db.Column(db.Integer)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    usuario = db.relationship('Favoritos', backref= 'usuario', lazy=True)

    def __repr__(self):
        return '<Usuario %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
        
class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # favoritos_id = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    vehiculos_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'))

    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personajes_id": self.personajes_id,
            "planetas_id": self.planetas_id,
            "vehicles_id": self.vehicles_id
            # do not serialize the password, its a security breach
        }

class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # perosnajes_id = db.Column(db.Integer)
    name = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    personajes = db.relationship('Favoritos', backref='personajes', lazy=True)


    def __repr__(self):
        return '<Personajes %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "personajes": self.personajes,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            # do not serialize the password, its a security breach
        }

class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # planetas_id = db.Column(db.Integer)
    name = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    planetas = db.relationship('Favoritos', backref='planetas', lazy=True)

    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planetas": self.planetas,
            "name": self.name,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            # do not serialize the password, its a security breach
        }

class Vehiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # vehiculos_id = db.Column(db.Integer)
    model = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    length = db.Column(db.String(250))
    crew = db.Column(db.String(250))
    vehiculos = db.relationship('Favoritos', backref='vehiculos', lazy=True)

    def __repr__(self):
        return '<Vehiculos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "vehiculos": self.vehiculos,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "crew": self.crew,
            # do not serialize the password, its a security breach
        } 