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

    [sqlite]  ; used when server_type == sqlite
    filename = movie.db

    [agent]
    model = qwen-plus
    api_key = {your api key}
    base_url = https://dashscope.aliyuncs.com/compatible-mode/v1
    ```
- 安装所需python包，推荐3.10
    ```python
    pip install -r requirements.txt
    ```
- 运行`run.py`

## 实现

- 数据库： 在 mysql 上测试
- 编程语言：Python
- Web 框架：Flask
- 前端框架：Bootstrap5

## 内容
- 完全重构了数据库模式, 使其符合课程要求及 3NF
- 修改了界面样式
- 添加了 Ai Agent 功能
