from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------
# USER
# ----------------------------

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    favorite_planets = db.relationship('FavoritePlanet', backref='user', cascade="all, delete-orphan")
    favorite_people = db.relationship('FavoritePeople', backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User id={self.id} email={self.email!r}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }

# ----------------------------
# PLANET
# ----------------------------

class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)

    residents = db.relationship('People', backref='planet', cascade="all, delete-orphan")
    favorites = db.relationship('FavoritePlanet', backref='planet', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Planet id={self.id} name={self.name!r}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }

# ----------------------------
# PEOPLE
# ----------------------------

class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    favorites = db.relationship('FavoritePeople', backref='people', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<People id={self.id} name={self.name!r}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "planet_id": self.planet_id
        }

# ----------------------------
# FAVORITE PLANETS
# ----------------------------

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'planet_id', name='unique_user_planet'),
    )

    def __repr__(self):
        return f'<FavoritePlanet id={self.id} user_id={self.user_id} planet_id={self.planet_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

# ----------------------------
# FAVORITE PEOPLE
# ----------------------------

class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'people_id', name='unique_user_people'),
    )

    def __repr__(self):
        return f'<FavoritePeople id={self.id} user_id={self.user_id} people_id={self.people_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id
        }
