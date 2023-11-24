from src import app, db
from src.db import MovieInfo, MovieBox, ActorInfo, MovieActorRelation

@app.route('/', methods=['GET', 'POST'])
def index():
    user = User.query.first()# 利用外键找到user的movie单
    # 这里先认为只有一个用户
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year, user_id = user.id)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    
    movies = Movie.query.filter_by(user_id = user.id).all()
    return render_template('index.html', movies=movies)