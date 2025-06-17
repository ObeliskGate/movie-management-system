from wtforms import StringField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, InputRequired
from flask_wtf import FlaskForm
from src.init import db

# 出品公司模型
class ProductionCompany(db.Model):
    __tablename__ = "production_company"
    company_id = db.Column(db.Integer, primary_key=True, nullable=False)
    company_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(20))
    movies = db.relationship("MovieInfo", backref="production_company", cascade="all, delete-orphan")

# 导演模型
class DirectorInfo(db.Model):
    __tablename__ = "director_info"
    director_id = db.Column(db.Integer, primary_key=True, nullable=False)
    director_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(20))
    movies = db.relationship("MovieInfo", secondary="movie_director_relation", back_populates="directors")

# 电影模型
class MovieInfo(db.Model):
    __tablename__ = "movie_info"
    movie_id = db.Column(db.Integer, primary_key=True, nullable=False)
    movie_name = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date)
    country = db.Column(db.String(20))
    type = db.Column(db.String(20))
    year = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('production_company.company_id'), nullable=False)
    actors = db.relationship("ActorInfo", secondary="role_info", back_populates="movies")
    directors = db.relationship("DirectorInfo", secondary="movie_director_relation", back_populates="movies")
    roles = db.relationship("RoleInfo", backref="movie", cascade="all, delete-orphan")

# 演员模型
class ActorInfo(db.Model):
    __tablename__ = "actor_info"
    actor_id = db.Column(db.Integer, primary_key=True, nullable=False)
    actor_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(20))
    movies = db.relationship("MovieInfo", secondary="role_info", back_populates="actors")
    roles = db.relationship("RoleInfo", backref="actor", cascade="all, delete-orphan")

# 角色模型
class RoleInfo(db.Model):
    __tablename__ = "role_info"
    role_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie_info.movie_id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor_info.actor_id'), nullable=False)
    role_name = db.Column(db.String(50), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('movie_id', 'actor_id', name='uq_movie_actor'),
    )

# 导演-电影关联模型
class MovieDirectorRelation(db.Model):
    __tablename__ = "movie_director_relation"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie_info.movie_id'), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director_info.director_id'), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('movie_id', 'director_id', name='uq_movie_director'),
    )

# ========== 表单类定义 ==========

# 演员表单类
class ActorForm(FlaskForm):
    actor_id = IntegerField('演员ID', validators=[InputRequired(), NumberRange(min=2000, max=1000000)])
    actor_name = StringField('演员姓名', validators=[InputRequired(), Length(max=50)])
    gender_choices = [('', '选择性别'),('男', '男'), ('女', '女')]
    gender = SelectField('性别', choices=gender_choices, validators=[InputRequired(), Length(max=10)])
    country = StringField('国家', validators=[InputRequired(), Length(max=20)])

class ActorSearchForm(FlaskForm):
    actor_id = IntegerField('演员ID', validators=[Optional()])
    actor_name = StringField('演员姓名', validators=[Optional(), Length(max=50)])
    gender_choices = [('', '选择性别'),('男', '男'), ('女', '女')]
    gender = SelectField('性别', choices=gender_choices, validators=[Optional()])
    country = StringField('国家', validators=[Length(max=20), Optional()])

class ActorEditForm(FlaskForm):
    actor_id = IntegerField('演员ID', validators=[NumberRange(min=2000, max=1000000)])
    actor_name = StringField('演员姓名', validators=[InputRequired(), Length(max=50)])
    gender_choices = [('', '选择性别'),('男', '男'), ('女', '女')]
    gender = SelectField('性别', choices=gender_choices, validators=[InputRequired(), Length(max=10)])
    country = StringField('国家', validators=[InputRequired(), Length(max=20)])

# 导演表单类
class DirectorForm(FlaskForm):
    director_id = IntegerField('导演ID', validators=[InputRequired(), NumberRange(min=3000, max=1000000)])
    director_name = StringField('导演姓名', validators=[InputRequired(), Length(max=50)])
    gender_choices = [('', '选择性别'),('男', '男'), ('女', '女')]
    gender = SelectField('性别', choices=gender_choices, validators=[InputRequired(), Length(max=10)])
    country = StringField('国家', validators=[InputRequired(), Length(max=20)])

class DirectorSearchForm(FlaskForm):
    director_id = IntegerField('导演ID', validators=[Optional()])
    director_name = StringField('导演姓名', validators=[Optional(), Length(max=50)])
    gender_choices = [('', '选择性别'),('男', '男'), ('女', '女')]
    gender = SelectField('性别', choices=gender_choices, validators=[Optional()])
    country = StringField('国家', validators=[Length(max=20), Optional()])

class DirectorEditForm(FlaskForm):
    director_id = IntegerField('导演ID', validators=[NumberRange(min=3000, max=1000000)])
    director_name = StringField('导演姓名', validators=[InputRequired(), Length(max=50)])
    gender_choices = [('', '选择性别'),('男', '男'), ('女', '女')]
    gender = SelectField('性别', choices=gender_choices, validators=[InputRequired(), Length(max=10)])
    country = StringField('国家', validators=[InputRequired(), Length(max=20)])

# 出品公司表单类
class CompanyForm(FlaskForm):
    company_id = IntegerField('公司ID', validators=[InputRequired(), NumberRange(min=4000, max=1000000)])
    company_name = StringField('公司名称', validators=[InputRequired(), Length(max=50)])
    city = StringField('城市', validators=[InputRequired(), Length(max=20)])

class CompanySearchForm(FlaskForm):
    company_id = IntegerField('公司ID', validators=[Optional()])
    company_name = StringField('公司名称', validators=[Optional(), Length(max=50)])
    city = StringField('城市', validators=[Length(max=20), Optional()])

class CompanyEditForm(FlaskForm):
    company_id = IntegerField('公司ID', validators=[NumberRange(min=4000, max=1000000)])
    company_name = StringField('公司名称', validators=[InputRequired(), Length(max=50)])
    city = StringField('城市', validators=[InputRequired(), Length(max=20)])

# 角色表单类
class RoleForm(FlaskForm):
    role_id = IntegerField('角色ID', validators=[InputRequired(), NumberRange(min=5000, max=1000000)])
    movie_id = IntegerField('电影ID', validators=[InputRequired()])
    actor_id = IntegerField('演员ID', validators=[InputRequired()])
    role_name = StringField('角色名称', validators=[InputRequired(), Length(max=50)])

class RoleSearchForm(FlaskForm):
    role_id = IntegerField('角色ID', validators=[Optional()])
    movie_id = IntegerField('电影ID', validators=[Optional()])
    actor_id = IntegerField('演员ID', validators=[Optional()])
    role_name = StringField('角色名称', validators=[Optional(), Length(max=50)])

class RoleEditForm(FlaskForm):
    role_id = IntegerField('角色ID', validators=[NumberRange(min=5000, max=1000000)])
    movie_id = IntegerField('电影ID', validators=[InputRequired()])
    actor_id = IntegerField('演员ID', validators=[InputRequired()])
    role_name = StringField('角色名称', validators=[InputRequired(), Length(max=50)])

# 电影表单类
class MovieForm(FlaskForm):
    movie_id = IntegerField('电影ID', validators=[InputRequired(), NumberRange(min=1000, max=1000000)])
    movie_name = StringField('电影名称', validators=[InputRequired(),Length(max=20)])
    release_date = DateField('上映日期', format=r'%Y-%m-%d', validators=[InputRequired()])
    country = StringField('国家', validators=[InputRequired(),Length(max=20)])
    type = StringField('类型', validators=[InputRequired()])
    company_id = IntegerField('出品公司ID', validators=[InputRequired()])

class MovieSearchForm(FlaskForm):   
    movie_id = IntegerField('电影ID', validators=[Optional()])
    movie_name = StringField('电影名称', validators=[Length(max=20)])
    release_date = DateField('上映日期', format=r'%Y-%m-%d', validators=[Optional()])
    country = StringField('国家', validators=[Length(max=20)])
    type = StringField('类型', validators=[Optional()])
    company_id = IntegerField('出品公司ID', validators=[Optional()])

class MovieEditForm(FlaskForm):
    movie_id = IntegerField('电影ID', validators=[NumberRange(min=1000, max=1000000)])
    movie_name = StringField('电影名称', validators=[InputRequired(),Length(max=20)])
    release_date = DateField('上映日期', format=r'%Y-%m-%d', validators=[InputRequired()])
    country = StringField('国家', validators=[InputRequired(),Length(max=20)])
    type = StringField('类型', validators=[InputRequired()])
    company_id = IntegerField('出品公司ID', validators=[InputRequired()])