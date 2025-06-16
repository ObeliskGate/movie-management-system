from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask import Flask
import configparser
import os
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

server_type = config.get('default','server_type',fallback='sqlite')

if server_type == 'SQL server':
    user, password,server,db_name=[value for _, value in config.items('Server')]

    app.config["SQLALCHEMY_DATABASE_URI"] = f'mssql+pymssql://{user}:{password}@{server}/{db_name}?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
    app.config['SECRET_KEY'] = 'your_secret_key'
    db = SQLAlchemy(app) 

elif server_type == 'sqlite':
    filename = config.get('sqlite','filename')
    db_path = os.path.join(os.getcwd(), filename)
    app.config["SQLALCHEMY_DATABASE_URI"] = rf"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

    app.config['SECRET_KEY'] = 'your_secret_key'
    db = SQLAlchemy(app) 

else:
    print('请填写config.ini选择数据库')
    exit()

def get_db():
    """Get the database instance."""
    return db

def db_connect_check():
    '''
    check whether to connect movieDB from SQL server'''
    with app.app_context():
        try:
            db.engine.connect()
            print(f"成功连接到{server_type}数据库")
            return True
        except OperationalError as e:
            print("无法连接到数据库")
            print(e.orig.args[0][1].decode('utf-8'))
            exit(0)
            return False
        
if __name__ == '__main__':
    db_connect_check()