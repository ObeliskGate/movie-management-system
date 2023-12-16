from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask import Flask

app = Flask(__name__)
db_name = 'movieDBtest'
app.config["SQLALCHEMY_DATABASE_URI"] = f'mssql+pymssql://sa:123456@DESKTOP-4KEIUAR/{db_name}?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app) 

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
        
if __name__ == '__main__':
    db_connect_check()