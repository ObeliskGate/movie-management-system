
from flask import Flask, render_template
from flask import request, url_for, redirect, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.exc import OperationalError
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Optional
from flask_bootstrap import Bootstrap
from flask import render_template, flash
from flask_wtf.csrf import CSRFError

#使用Bootstrap4 

app = Flask(__name__)
db_name = 'movieDBtest'
app.config["SQLALCHEMY_DATABASE_URI"] = f'mssql+pymssql://sa:123456@DESKTOP-4KEIUAR/{db_name}?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app) 
bootstrap = Bootstrap5(app)  

class MovieInfo(db.Model):
    __tablename__ = "movie_info"

    movie_id = db.Column(db.String(10), primary_key=True, nullable=False)
    movie_name = db.Column(db.String(20), nullable=False)
    release_date = db.Column(db.DateTime)
    country = db.Column(db.String(20))
    type = db.Column(db.String(10))
    year = db.Column(db.Integer, CheckConstraint('year>=1000 and year<=2100'))

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
    actor_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(20))

class MovieForm(FlaskForm):
    movie_name = StringField('Movie Name', validators=[DataRequired(), Length(max=20)])
    release_date = DateField('Release Date', format='%Y-%m-%d', validators=[Optional()])
    country = StringField('Country', validators=[Length(max=20)])
    type = StringField('Type', validators=[Optional()])
    year = IntegerField('Year')

def db_connect_check():
    '''
    check whether to connect movieDB from SQL server'''
    with app.app_context():
        try:
            db.engine.connect()
            print(f"成功连接到数据库{db_name}")
            return True
        except OperationalError as e:
            print("无法连接到数据库")
            print(e.orig.args[0][1].decode('utf-8'))
            exit(0)
            return False

@app.route('/edit_movie/<movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)
    form = MovieForm(obj=movie)

    if form.validate_on_submit():
        movie.year = form.release_date.data.year

        form.populate_obj(movie)
        db.session.commit()
        flash(f'成功修改编号为{movie_id}的电影信息！', 'success')
        return redirect(url_for('index'))

    return render_template('edit_movie.html', form=form, movie=movie)

# 删除
@app.route('/delete_movie/<movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete_movie(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.',"success")
    return redirect(url_for('index'))  # 重定向回主页

# 搜索
@app.route('/search_movie', methods=['GET', 'POST'])
def search_movie():
    form = MovieForm()

    if request.method == 'POST' and form.validate_on_submit():
        movie_name = form.movie_name.data
        release_date = form.release_date.data
        country = form.country.data
        movie_type = form.type.data
        year = form.year.data

        # Query the database based on the form data
        query = MovieInfo.query
        if movie_name:
            query = query.filter(MovieInfo.movie_name.ilike(f'%{movie_name}%'))
        if release_date:
            query = query.filter(MovieInfo.release_date == release_date)
        if country:
            query = query.filter(MovieInfo.country.ilike(f'%{country}%'))
        if movie_type:
            query = query.filter(MovieInfo.type.ilike(f'%{movie_type}%'))
        if year:
            query = query.filter(MovieInfo.year == year)

        results = query.all()

        return render_template('search_movie.html', form=form, results=results)

    return render_template('search_movie.html', form=form, results=None)



@app.context_processor
def inject_user():  # 函数名可以随意修改
    # 获取 User 表中所有独一值
    # 让movie外键user_id进行选择，否则无法提交，会报错
    m = MovieInfo.query.all()
    mc = MovieInfo.__table__.columns.keys()
    return dict(movies=m,movies_col = mc) 

@app.route('/')
def index():
    return render_template('table.html')

if __name__ == '__main__':
    db_connect_check()
    app.run(port=1234,debug=True)
    with app.app_context():
        ...
    ...