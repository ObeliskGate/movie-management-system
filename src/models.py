from wtforms import StringField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, InputRequired
from flask_wtf import FlaskForm
from src.init import db

# 出品公司模型
class ProductionCompany(db.Model):
    __tablename__ = "production_company"
    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(20))
    movies = db.relationship("MovieInfo", backref="production_company", cascade="all, delete-orphan")

# 演员-电影关系表
actor_movie_relation = db.Table('actor_movie_relation',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor_info.actor_id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie_info.movie_id'), primary_key=True)
)

# 导演-电影关系表
director_movie_relation = db.Table('director_movie_relation',
    db.Column('director_id', db.Integer, db.ForeignKey('director_info.director_id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie_info.movie_id'), primary_key=True)
)


# 演员模型
class ActorInfo(db.Model):
    __tablename__ = "actor_info"
    actor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor_name = db.Column(db.String(50), nullable=False)
    # 修改点：将 gender 改为 type
    type = db.Column(db.String(20), nullable=False)  # 改为类型字段
    country = db.Column(db.String(20))
    movies = db.relationship("MovieInfo", 
                             secondary=actor_movie_relation,
                             back_populates="actors")
    roles = db.relationship("RoleInfo", backref="actor", cascade="all, delete-orphan")

# 导演模型
class DirectorInfo(db.Model):
    __tablename__ = "director_info"
    director_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    director_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(20))
    # 更新关系：导演与电影的多对多关系
    movies = db.relationship("MovieInfo", 
                             secondary=director_movie_relation,
                             back_populates="directors")

# 电影模型
class MovieInfo(db.Model):
    __tablename__ = "movie_info"
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date)
    country = db.Column(db.String(20))
    type = db.Column(db.String(20))
    year = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('production_company.company_id'), nullable=False)

    actors = db.relationship("ActorInfo", 
                             secondary=actor_movie_relation,
                             back_populates="movies")
    
    directors = db.relationship("DirectorInfo", 
                                secondary=director_movie_relation,
                                back_populates="movies")
    
    roles = db.relationship("RoleInfo", backref="movie", cascade="all, delete-orphan")

# 角色模型
class RoleInfo(db.Model):
    __tablename__ = "role_info"
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    actor_name = StringField('演员姓名', validators=[InputRequired(), Length(max=50)])
    type_choices = [('', '选择类型'),('男', '男'), ('女', '女'), ('动物', '动物'), ('旁白', '旁白')]
    type = SelectField('类型', choices=type_choices, validators=[InputRequired(), Length(max=20)])
    country = StringField('国家', validators=[InputRequired(), Length(max=20)])

class ActorSearchForm(FlaskForm):
    actor_id = IntegerField('演员ID', validators=[Optional()])
    actor_name = StringField('演员姓名', validators=[Optional(), Length(max=50)])
    type_choices = [('', '选择类型'),('男', '男'), ('女', '女'), ('动物', '动物'), ('旁白', '旁白')]
    type = SelectField('类型', choices=type_choices, validators=[Optional()])
    country = StringField('国家', validators=[Length(max=20), Optional()])

class ActorEditForm(FlaskForm):
    actor_id = IntegerField('演员ID')#, validators=[NumberRange(min=2000, max=1000000)]
    actor_name = StringField('演员姓名', validators=[InputRequired(), Length(max=50)])
    type_choices = [('', '选择类型'),('男', '男'), ('女', '女'), ('动物', '动物'), ('旁白', '旁白')]
    type = SelectField('类型', choices=type_choices, validators=[InputRequired(), Length(max=20)])
    country = StringField('国家', validators=[InputRequired(), Length(max=20)])

# 导演表单类
class DirectorForm(FlaskForm):
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
    director_id = IntegerField('导演ID')#, validators=[NumberRange(min=3000, max=1000000)]
    director_name = StringField('导演姓名', validators=[InputRequired(), Length(max=50)])
    gender_choices = [('', '选择性别'),('男', '男'), ('女', '女')]
    gender = SelectField('性别', choices=gender_choices, validators=[InputRequired(), Length(max=10)])
    country = StringField('国家', validators=[InputRequired(), Length(max=20)])

# 出品公司表单类
class CompanyForm(FlaskForm):
    company_name = StringField('公司名称', validators=[InputRequired(), Length(max=50)])
    city = StringField('城市', validators=[InputRequired(), Length(max=20)])

class CompanySearchForm(FlaskForm):
    company_id = IntegerField('公司ID', validators=[Optional()])
    company_name = StringField('公司名称', validators=[Optional(), Length(max=50)])
    city = StringField('城市', validators=[Length(max=20), Optional()])

class CompanyEditForm(FlaskForm):
    company_id = IntegerField('公司ID')#, validators=[NumberRange(min=4000, max=1000000)]
    company_name = StringField('公司名称', validators=[InputRequired(), Length(max=50)])
    city = StringField('城市', validators=[InputRequired(), Length(max=20)])

# 角色表单类
class RoleForm(FlaskForm):
    movie_id = IntegerField('电影ID', validators=[InputRequired()])
    actor_id = IntegerField('演员ID', validators=[InputRequired()])
    role_name = StringField('角色名称', validators=[InputRequired(), Length(max=50)])

class RoleSearchForm(FlaskForm):
    role_id = IntegerField('角色ID', validators=[Optional()])
    movie_id = IntegerField('电影ID', validators=[Optional()])
    actor_id = IntegerField('演员ID', validators=[Optional()])
    role_name = StringField('角色名称', validators=[Optional(), Length(max=50)])

class RoleEditForm(FlaskForm):
    role_id = IntegerField('角色ID')#, validators=[NumberRange(min=5000, max=1000000)]
    movie_id = IntegerField('电影ID', validators=[InputRequired()])
    actor_id = IntegerField('演员ID', validators=[InputRequired()])
    role_name = StringField('角色名称', validators=[InputRequired(), Length(max=50)])

# 电影表单类
class MovieForm(FlaskForm):
    movie_name = StringField('电影名称', validators=[InputRequired(),Length(max=20)])
    release_date = DateField('上映日期', format=r'%Y-%m-%d', validators=[InputRequired()])
    country = StringField('国家', validators=[InputRequired(),Length(max=20)])
    type = StringField('类型', validators=[InputRequired()])
    company_id = IntegerField('出品公司ID', validators=[InputRequired()])
    actor_ids = StringField('演员ID列表', validators=[Optional()])
    director_ids = StringField('导演ID列表', validators=[Optional()])

class MovieSearchForm(FlaskForm):   
    movie_id = IntegerField('电影ID', validators=[Optional()])
    movie_name = StringField('电影名称', validators=[Length(max=20)])
    release_date = DateField('上映日期', format=r'%Y-%m-%d', validators=[Optional()])
    country = StringField('国家', validators=[Length(max=20)])
    type = StringField('类型', validators=[Optional()])
    company_id = IntegerField('出品公司ID', validators=[Optional()])

class MovieEditForm(FlaskForm):
    movie_name = StringField('电影名称')#, validators=[InputRequired(),Length(max=20)]
    release_date = DateField('上映日期', format=r'%Y-%m-%d', validators=[InputRequired()])
    country = StringField('国家', validators=[InputRequired(),Length(max=20)])
    type = StringField('类型', validators=[InputRequired()])
    company_id = IntegerField('出品公司ID', validators=[InputRequired()])
    # 添加以下两个字段
    actor_ids = StringField('演员ID列表', validators=[Optional()])
    director_ids = StringField('导演ID列表', validators=[Optional()])