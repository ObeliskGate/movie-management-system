from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask import Flask

from models_connect import SQLiteForm,SQLServerForm
from flask import render_template, redirect, url_for, flash

app = Flask(__name__)
# db_name = 'movieDBtest'
# app.config["SQLALCHEMY_DATABASE_URI"] = f'mssql+pymssql://sa:123456@DESKTOP-4KEIUAR/{db_name}?charset=utf8'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'init'
db = SQLAlchemy() 

def sqlserver_connect(form):
    global app,db
    
    server = form.server.data
    user = form.user.data
    password = form.user.data
    database = form.database.data
    # self.app.config["SQLALCHEMY_DATABASE_URI"] = f'mssql+pymssql://{user}:{password}@{server}/{database}?charset=utf8'
    # self.app.config['SECRET_KEY'] = 'your_secret_key' 
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f'mssql+pymssql://{user}:{password}@{server}/{database}?charset=utf8'
    app.config['SECRET_KEY'] = 'sqlserver'

    with app.app_context():
        db.init_app(app) 
        try:
            db.engine.connect()
            print(f"成功连接到SQL server数据库{database}")
            return True
        except OperationalError as e:
            print("无法连接到SQL server数据库")
            print(e.orig.args[0][1].decode('utf-8'))
            # exit(0)
            return False
def sqlite_connect(liteform):
    file_path = liteform.file_path.data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://{app.root_path}/ {file_path}'
    return False
# class db_connect:
#     global app,db
#     # def __init__(self):
#     #     '''方便在外部引用app,db'''
#     #     self.app = Flask(__name__)
#     #     self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#     def sqlserver(self,form):
#         global app,db

#         server = form.server.data
#         user = form.user.data
#         password = form.user.data
#         database = form.database.data
#         # self.app.config["SQLALCHEMY_DATABASE_URI"] = f'mssql+pymssql://{user}:{password}@{server}/{database}?charset=utf8'
#         # self.app.config['SECRET_KEY'] = 'your_secret_key' 
        
#         app.config["SQLALCHEMY_DATABASE_URI"] = f'mssql+pymssql://{user}:{password}@{server}/{database}?charset=utf8'
#         app.config['SECRET_KEY'] = 'sqlserver'

#         with app.app_context():
#             db = SQLAlchemy(app) 
#             try:
#                 db.engine.connect()
#                 print(f"成功连接到SQL server数据库{database}")
#                 return True
#             except OperationalError as e:
#                 print("无法连接到SQL server数据库")
#                 print(e.orig.args[0][1].decode('utf-8'))
#                 # exit(0)
#                 return False
#     def sqlite(self,liteform):
#         file_path = liteform.file_path.data
#         app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://{app.root_path}/ {file_path}'

#         ...
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://C:/Users/Administrator/Desktop/base.db'

# @app.route('/',methods=['GET', 'POST'])
# def index():
#     form = SQLServerForm()
#     liteform = SQLiteForm()
#     # connect = db_connect()
#     # if connect.sqlserver(form):
#     #     print(111)
#     if form.validate_on_submit() and sqlserver(form):
#         db_connect_flag = True
#         flash(f'成功连接到SQL server数据库{form.database.data}',"info")
#         return redirect(url_for('index'))
#     elif liteform.validate_on_submit() and sqlite(liteform):
#         db_connect_flag = True
#         flash(f'成功连接到SQLite数据库{liteform.file_root.data}',"info")
#         return redirect(url_for('index'))
#     else:
#         db_connect_flag = False
#         # flash(f'连接失败',"warning")
#         return render_template('index.html',form=form,liteform = liteform,db_connect_flag=db_connect_flag)

from models_connect import SQLiteForm,SQLServerForm
from init0 import sqlserver_connect,sqlite_connect
@app.route('/',methods=['GET', 'POST'])
def index():
    form = SQLServerForm()
    liteform = SQLiteForm()
    # connect = db_connect()
    # if connect.sqlserver(form):
    #     print(111)
    if form.validate_on_submit() and sqlserver_connect(form):
        db_connect_flag = True
        flash(f'成功连接到SQL server数据库{form.database.data}',"info")
        return redirect(url_for('index'))
    elif liteform.validate_on_submit() and sqlite_connect(liteform):
        db_connect_flag = True
        flash(f'成功连接到SQLite数据库{liteform.file_root.data}',"info")
        return redirect(url_for('index'))
    else:
        db_connect_flag = False
        # flash(f'连接失败',"warning")
        return render_template('index.html',form=form,liteform = liteform,db_connect_flag=db_connect_flag)

if __name__ == '__main__':
    app.run(port=1111,debug=True)