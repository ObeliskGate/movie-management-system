from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask import Flask
import configparser
import os
import pymysql

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 创建Flask应用
app = Flask(__name__)

# 获取服务器类型配置
server_type = config.get('default', 'server_type', fallback='sqlite')

# 数据库连接池配置
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_size": 20,
    "max_overflow": 30
}

if server_type == 'mysql':
    # MySQL配置
    host = config.get('mysql', 'host')
    port = config.getint('mysql', 'port', fallback=3306)
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    db_name = config.get('mysql', 'db_name')
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    db = SQLAlchemy(app)

elif server_type == 'sqlite':
    # SQLite配置
    filename = config.get('sqlite', 'filename')
    db_path = os.path.join(os.getcwd(), filename)
    app.config["SQLALCHEMY_DATABASE_URI"] = rf"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    db = SQLAlchemy(app)

else:
    print('请填写config.ini选择数据库')
    exit()

def db_connect_check():
    """数据库连接检查"""
    with app.app_context():
        try:
            db.engine.connect()
            print(f"成功连接到{server_type}数据库")
            return True
        except OperationalError as e:
            print("无法连接到数据库")
            print(str(e))
            exit(0)
            return False

if __name__ == '__main__':
    db_connect_check()