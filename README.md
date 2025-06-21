# 电影管理系统movie management system

Fudan SDS 《数据库及实现》课程期末 Project.

## 使用
- 在根目录下添加`config.ini`, e.g.
    ```
    [default]
    server_type = mysql
    secret_key = {default secret key}

    [mysql]
    host = localhost
    port = 3306
    user = {root}
    password = {your password}
    db_name = movie_db

    [sqlite]
    filename = movie.db

    [agent]
    model = qwen-plus
    api_key = {your api key}
    base_url = https://dashscope.aliyuncs.com/compatible-mode/v1
    ```
- 安装所需python包，推荐3.10
    ```
    pip install -r requirements.txt
    ```
- 运行`python run.py`

### 注意事项
- 我们的测试数据位于`movie_init.sql`中, 在 mysql 中没有`db_name`数据库时会自动执行该`.sql`文件, 否则会从. 若希望从头测试, 请`DROP DATABASE db_name`或设置一个和已有表`db_name`
- `sqlite`通过本地的`filename`文件初始化, 需要自行通过`movie_init.sql`构造`.db`文件


## 实现

- 数据库： 在 mysql 上测试, 支持 sqlite
- 编程语言：Python
- Web 框架：Flask
- 前端框架：Bootstrap5
