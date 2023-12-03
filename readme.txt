
sql server默认的字符集
中国默认的排序规则 Chinese_PRC_CI_AS
对应的代码页就是 cp936，在操作系统字符集系统中反应出来的字符集就是 GBK。因而会导致乱码

ALTER DATABASE movieDB
COLLATE chinese_simplified_pinyin_100_ci_AS_sc_utf8

此外，为了保证完全输入，加大了部分列的vchar为50


用<a type="button" class="btn btn-outline-success"
href="{{ url_for('edit_movie', movie_id=movie.movie_id) }}">Edit</a>
<a >连接按钮操作


url_for('edit_movie', movie_id=movie.movie_id)将操作连接到视图函数
@app.route('/edit_movie/<movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
中，这一步传递了参数movie_id


    <!-- 插入提示框 -->
    <!-- 
        get_flashed_messages()是一个列表，该列表可以取出闪现信息，该条闪现信息只要被取出就会删除掉。 
        -设置：flash('用户名错误', "username_error")
      flash('用户密码错误', "password_error") # 第二个参数为闪现信息的分类。
        -取所有闪现信息的类别和闪现内容：get_flashed_messages(with_categories=True)
        -针对分类过滤取值：get_flashed_messages(category_filter=['username_error']) 
                    # 中括号内可以写多个分类。
        -注意：如果flash()没有传入第二个参数进行分类，默认分类是 'message'
    -->
模板取值：   {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
            <ul class=flashes>
            {% for category, message in messages %}


使用模态弹框（Modal）、警告框（Alerts）等组件极大美化网页可读性