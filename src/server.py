from flask import render_template, redirect, url_for, flash, request
from src.init import db_connect_check, app, db
from src.models import *
from src.pipeline import *
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask import render_template, redirect, url_for, flash
from src.init import db_connect_check, app, db, server_type
from src.models import *
from src.pipeline import *
from src.autogen_multi import set_chat_route

set_chat_route(app)

# 错误处理
@app.errorhandler(IntegrityError)
def handle_integrity_error(e):
    db.session.rollback()
    flash('数据库操作失败：数据冲突或约束违规', 'danger')
    return redirect(request.referrer or url_for('index'))

@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    db.session.rollback()
    flash('数据库操作失败，请重试', 'danger')
    return redirect(request.referrer or url_for('index'))

# 电影管理路由
@app.route('/movie', methods=['GET', 'POST'])
def movie():
    form = MovieForm()
    if form.validate_on_submit():
        flag, message = movie_add_pipeline(form)
        flash(message, 'success' if flag else 'danger')
        return redirect(url_for('movie'))
    return render_template('movie.html', form=form)

@app.route('/movie_edit/<int:movie_id>', methods=['GET', 'POST'])
def movie_edit(movie_id):
    movie = MovieInfo.query.get_or_404(movie_id)
    form = MovieEditForm(obj=movie)
    
    if form.validate_on_submit():
        movie.movie_id = form.movie_id.data
        movie.movie_name = form.movie_name.data
        movie.release_date = form.release_date.data
        movie.country = form.country.data
        movie.type = form.type.data
        movie.year = form.release_date.data.year
        movie.company_id = form.company_id.data
        
        try:
            db.session.commit()
            flash(f'成功修改电影 {movie.movie_name} (ID:{movie_id})', 'success')
            return redirect(url_for('movie'))
        except IntegrityError:
            flash('修改失败：ID冲突或数据错误', 'danger')
    
    return render_template('movie_edit.html', form=form, movie=movie)

@app.route('/movie_delete/<int:movie_id>', methods=['POST'])
def movie_delete(movie_id):
    flag, message = safe_delete(MovieInfo, movie_id, 'movie_id')
    flash(message, 'success' if flag else 'danger')
    return redirect(url_for('movie'))

@app.route('/movie_search', methods=['GET', 'POST'])
def movie_search():
    form = MovieSearchForm()
    results = None
    if form.validate_on_submit():
        results = movie_search_pipeline(form)
    return render_template('movie_search.html', form=form, results=results)

# 演员管理路由
@app.route('/actor', methods=['GET', 'POST'])
def actor():
    form = ActorForm()
    if form.validate_on_submit():
        flag, message = actor_add_pipeline(form)
        flash(message, 'success' if flag else 'danger')
        return redirect(url_for('actor'))
    return render_template('actor.html', form=form)

@app.route('/actor_edit/<int:actor_id>', methods=['GET', 'POST'])
def actor_edit(actor_id):
    actor = ActorInfo.query.get_or_404(actor_id)
    form = ActorEditForm(obj=actor)
    
    if form.validate_on_submit():
        form.populate_obj(actor)
        db.session.commit()
        flash(f'成功修改演员 {actor.actor_name} (ID:{actor_id})', 'success')
        return redirect(url_for('actor'))
    return render_template('actor_edit.html', form=form, actor=actor)

@app.route('/actor_delete/<int:actor_id>', methods=['POST'])
def actor_delete(actor_id):
    flag, message = safe_delete(ActorInfo, actor_id, 'actor_id')
    flash(message, 'success' if flag else 'danger')
    return redirect(url_for('actor'))

@app.route('/actor_search', methods=['GET', 'POST'])
def actor_search():
    form = ActorSearchForm()
    results = None
    if form.validate_on_submit():
        results = actor_search_pipeline(form)
    return render_template('actor_search.html', form=form, results=results)

# 导演管理路由
@app.route('/director', methods=['GET', 'POST'])
def director():
    form = DirectorForm()
    if form.validate_on_submit():
        flag, message = director_add_pipeline(form)
        flash(message, 'success' if flag else 'danger')
        return redirect(url_for('director'))
    return render_template('director.html', form=form)

@app.route('/director_edit/<int:director_id>', methods=['GET', 'POST'])
def director_edit(director_id):
    director = DirectorInfo.query.get_or_404(director_id)
    form = DirectorEditForm(obj=director)
    
    if form.validate_on_submit():
        form.populate_obj(director)
        db.session.commit()
        flash(f'成功修改导演 {director.director_name} (ID:{director_id})', 'success')
        return redirect(url_for('director'))
    return render_template('director_edit.html', form=form, director=director)

@app.route('/director_delete/<int:director_id>', methods=['POST'])
def director_delete(director_id):
    flag, message = safe_delete(DirectorInfo, director_id, 'director_id')
    flash(message, 'success' if flag else 'danger')
    return redirect(url_for('director'))

@app.route('/director_search', methods=['GET', 'POST'])
def director_search():
    form = DirectorSearchForm()
    results = None
    if form.validate_on_submit():
        results = director_search_pipeline(form)
    return render_template('director_search.html', form=form, results=results)

# 出品公司管理路由
@app.route('/company', methods=['GET', 'POST'])
def company():
    form = CompanyForm()
    if form.validate_on_submit():
        flag, message = company_add_pipeline(form)
        flash(message, 'success' if flag else 'danger')
        return redirect(url_for('company'))
    return render_template('company.html', form=form)

@app.route('/company_edit/<int:company_id>', methods=['GET', 'POST'])
def company_edit(company_id):
    company = ProductionCompany.query.get_or_404(company_id)
    form = CompanyEditForm(obj=company)
    
    if form.validate_on_submit():
        form.populate_obj(company)
        db.session.commit()
        flash(f'成功修改出品公司 {company.company_name} (ID:{company_id})', 'success')
        return redirect(url_for('company'))
    return render_template('company_edit.html', form=form, company=company)

@app.route('/company_delete/<int:company_id>', methods=['POST'])
def company_delete(company_id):
    flag, message = safe_delete(ProductionCompany, company_id, 'company_id')
    flash(message, 'success' if flag else 'danger')
    return redirect(url_for('company'))

@app.route('/company_search', methods=['GET', 'POST'])
def company_search():
    form = CompanySearchForm()
    results = None
    if form.validate_on_submit():
        results = company_search_pipeline(form)
    return render_template('company_search.html', form=form, results=results)

# 角色管理路由
@app.route('/role', methods=['GET', 'POST'])
def role():
    form = RoleForm()
    if form.validate_on_submit():
        flag, message = role_add_pipeline(form)
        flash(message, 'success' if flag else 'danger')
        return redirect(url_for('role'))
    return render_template('role.html', form=form)

@app.route('/role_edit/<int:role_id>', methods=['GET', 'POST'])
def role_edit(role_id):
    role = RoleInfo.query.get_or_404(role_id)
    form = RoleEditForm(obj=role)
    
    if form.validate_on_submit():
        form.populate_obj(role)
        db.session.commit()
        flash(f'成功修改角色 {role.role_name} (ID:{role_id})', 'success')
        return redirect(url_for('role'))
    return render_template('role_edit.html', form=form, role=role)

@app.route('/role_delete/<int:role_id>', methods=['POST'])
def role_delete(role_id):
    flag, message = safe_delete(RoleInfo, role_id, 'role_id')
    flash(message, 'success' if flag else 'danger')
    return redirect(url_for('role'))

@app.route('/role_search', methods=['GET', 'POST'])
def role_search():
    form = RoleSearchForm()
    results = None
    if form.validate_on_submit():
        results = role_search_pipeline(form)
    return render_template('role_search.html', form=form, results=results)

# 查询功能路由
@app.route('/director_movies/<int:director_id>')
def director_movies(director_id):
    movies = director_movies_pipeline(director_id)
    if movies is None:
        flash(f"未找到导演ID {director_id}", "warning")
        return redirect(url_for('director'))
    return render_template('director_movies.html', director_id=director_id, movies=movies)

@app.route('/actor_movies/<int:actor_id>')
def actor_movies(actor_id):
    movies = actor_movies_pipeline(actor_id)
    if movies is None:
        flash(f"未找到演员ID {actor_id}", "warning")
        return redirect(url_for('actor'))
    return render_template('actor_movies.html', actor_id=actor_id, movies=movies)

@app.route('/role_info/<int:role_id>')
def role_info(role_id):
    role = role_info_pipeline(role_id)
    if not role:
        flash(f"未找到角色ID {role_id}", "warning")
        return redirect(url_for('role'))
    return render_template('role_info.html', role=role)


# 全局上下文处理器
@app.context_processor
def inject_user():
    return dict(
        movies=MovieInfo.query.all(),
        actors=ActorInfo.query.all(),
        directors=DirectorInfo.query.all(),
        companies=ProductionCompany.query.all(),
        roles=RoleInfo.query.all()
    )

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    db_connect_check()
    app.run(port=12345, debug=True)