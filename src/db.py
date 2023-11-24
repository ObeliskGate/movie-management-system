from sqlalchemy import CheckConstraint

from src import db

class MovieInfo(db.Model):
    __tablename__ = "movie_info"

    movie_id = db.Column(db.String(10), primary_key=True, nullable=False)
    movie_name = db.Column(db.String(20), nullable=False)
    release_date = db.Column(db.DateTime)
    country = db.Column(db.String(20))
    movie_type = db.Column(db.String(10))
    year = db.Column(db.Integer, CheckConstraint('year>=1000 and year<=2100'))


class MovieBox(db.Model):
    __tablename__ = "movie_box"

    movie_id = db.Column(db.String(10), primary_key=True, nullable=False)
    box = db.Column(db.Float)


class ActorInfo(db.Model):
    __tablename__ = "actor_info"

    actor_id = db.Column(db.String(10), primary_key=True, nullable=False)
    actor_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(20))

class MovieActorRelation(db.Model):
    __tablename__ = "movie_actor_relation"

    id = db.Column(db.String(10), primary_key=True, nullable=False)
    movie_id = db.Column(db.String(10), db.ForeignKey('movie_info.movie_id'), nullable=False)
    actor_id = db.Column(db.String(10), db.ForeignKey('actor_info.actor_id'), nullable=False)
    relation_type = db.Column(db.String(20))
