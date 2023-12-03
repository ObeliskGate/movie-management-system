from wtforms import StringField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from flask_wtf import FlaskForm
from init import db

class MovieInfo(db.Model):
    __tablename__ = "movie_info"

    movie_id = db.Column(db.String(10), primary_key=True, nullable=False)
    movie_name = db.Column(db.String(20), nullable=False)
    release_date = db.Column(db.DateTime)
    country = db.Column(db.String(20))
    type = db.Column(db.String(10))
    year = db.Column(db.Integer)

    # db.relationship("MovieActorRelation", backref = "MovieInfo")# 外键约束
    actors = db.relationship("MovieActorRelation", backref="movie_info", cascade="all, delete-orphan")# 外键约束，删除movie_info同时删除相应movie_actor_relation

class MovieActorRelation(db.Model):
    __tablename__ = "movie_actor_relation"

    id = db.Column(db.String(10), primary_key=True, nullable=False)
    movie_id = db.Column(db.String(10), db.ForeignKey('movie_info.movie_id'), nullable=False)
    # 在删除 "movie_info" 表中的记录时，自动删除与之相关的 "movie_actor_relation" 表中的记录
    actor_id = db.Column(db.String(10), db.ForeignKey('actor_info.actor_id'), nullable=False)
    relation_type = db.Column(db.String(20))


class MovieBox(db.Model):
    __tablename__ = "movie_box"

    movie_id = db.Column(db.String(10), primary_key=True, nullable=False)
    box = db.Column(db.Float)

class ActorInfo(db.Model):
    __tablename__ = "actor_info"

    actor_id = db.Column(db.String(10), primary_key=True, nullable=False)
    actor_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(20))

    movies = db.relationship("MovieActorRelation", backref="actor_info", cascade="all, delete-orphan")

class ActorForm(FlaskForm):
    actor_id = StringField('Actor ID', validators=[Optional(), Length(max=10)])
    actor_name = StringField('Actor Name', validators=[Optional(), Length(max=50)])
    gender = StringField('Gender', validators=[Optional()])
    country = StringField('Country', validators=[Length(max=20), Optional()])

class MovieForm(FlaskForm):
    movie_id = StringField('Movie ID')
    movie_name = StringField('Movie Name', validators=[Length(max=20)])
    release_date = DateField('Release Date', format=r'%Y-%m-%d', validators=[Optional()])
    country = StringField('Country', validators=[Length(max=20)])
    type = StringField('Type', validators=[Optional()])
    year = IntegerField('Year', validators=[NumberRange(min=2000,max=2100),Optional()])