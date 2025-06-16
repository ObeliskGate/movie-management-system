from flask import render_template, redirect, url_for, flash
# from init import db_connect_check,app,db
# from models import *
# from pipeline import *
from src.init import db_connect_check, app, db, server_type
from src.models import *
from src.pipeline import *

@app.route('/movie_edit/<movie_id>', methods=['GET', 'POST'])
def movie_edit(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)
    form = MovieEditForm(obj=movie)

    if form.validate_on_submit():
        movie.year = form.release_date.data.year
        form.populate_obj(movie)
        db.session.commit()
        flash(f'成功修改编号为{movie_id}的电影信息！', 'success')
        return redirect(url_for('movie'))
    return render_template('movie_edit.html', form=form, movie=movie)

# 删除
@app.route('/movie_delete/<movie_id>', methods=['POST'])
def movie_delete(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id) 
    db.session.delete(movie)
    db.session.commit() 
    flash(f'成功删除编号为{movie_id}的电影信息！',"success")
    return redirect(url_for('movie')) 

# 搜索
@app.route('/movie_search', methods=['GET', 'POST'])
def movie_search():
    form = MovieSearchForm()
    if form.validate_on_submit(): 
        return render_template('movie_search.html', form=form, results=movie_search_pipeline(form))
    return render_template('movie_search.html', form=form, results=None)


@app.route('/movie', methods=['GET', 'POST'])
def movie():
    form = MovieForm()
    if form.validate_on_submit():
        flag, message = movie_add_pipeline(form)
        if flag:
            flash(message, 'success')
        else:
            flash(message, 'warning')
        return redirect(url_for('movie'))
    return render_template('movie.html',form = form)

@app.route('/actor_delete/<actor_id>', methods=['POST'])  # 限定只接受 POST 请求
def actor_delete(actor_id):
    actor = ActorInfo.query.get_or_404(actor_id)  # 获取电影记录
    db.session.delete(actor)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话E
    flash(f'成功删除编号为{actor_id}的演员信息！',"success")
    return redirect(url_for('actor'))  # 重定向回主页

@app.route('/actor_search', methods=['GET', 'POST'])
def actor_search():
    form = ActorSearchForm()
    if form.validate_on_submit(): 
        return render_template('actor_search.html', form=form, results=actor_search_pipeline(form))
    return render_template('actor_search.html', form=form, results=None)



@app.route('/actor', methods=['GET', 'POST'])
def actor():
    form = ActorForm()
    if form.validate_on_submit():
        flag, message = actor_add_pipeline(form)
        if flag:
            flash(message, 'success')
        else:
            flash(message, 'warning')
        return redirect(url_for('actor'))
    return render_template('actor.html',form = form)

@app.route('/actor_edit/<actor_id>', methods=['GET', 'POST'])
def actor_edit(actor_id):
    actor = ActorInfo.query.get_or_404(actor_id)
    form = ActorEditForm(obj=actor)

    if form.validate_on_submit():
        form.populate_obj(actor)
        db.session.commit()
        flash(f'成功修改编号为{actor_id}的演员信息！', 'success')
        return redirect(url_for('actor'))
    return render_template('actor_edit.html', form=form, actor=actor)


@app.context_processor
def inject_user():  # 函数名可以随意修改，全局传入参数
    m = MovieInfo.query.all()
    mc = MovieInfo.__table__.columns.keys()
    a = ActorInfo.query.all()
    ac = ActorInfo.__table__.columns.keys()
    return dict(movies=m,movies_col = mc,actors=a,actors_col = ac) 

@app.route('/')
def index():
    return render_template('index.html',server_type = server_type)

if __name__ == '__main__':
    db_connect_check()
    app.run(port=12345,debug=True)
    with app.app_context():
        ...
    ...