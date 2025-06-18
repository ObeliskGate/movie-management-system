from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from flask import Flask
import configparser
import os
from pathlib import Path

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 创建Flask应用
app = Flask(__name__)

app.config['SECRET_KEY'] = config.get('default', 'secret_key', fallback='default_secret_key')

# 获取服务器类型配置
server_type = config.get('default', 'server_type', fallback='mysql')

# 数据库连接池配置
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_size": 20,
    "max_overflow": 30
}


def execute_sql_file(filename, connection):
    """执行SQL文件"""
    try:
        sql_path = Path(filename)
        if not sql_path.exists():
            print(f"SQL文件 {filename} 不存在")
            return False
            
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_commands = [text(f"{it.strip()};") for it in f.read().split(';') if it.strip()]
            
        with app.app_context():
            for command in sql_commands:
                connection.execute(command)
            connection.commit()
        print(f"成功执行SQL文件: {filename}")
        return True
    except Exception as e:
        print(f"执行SQL文件时出错: {str(e)}")
        return False

if server_type == 'mysql':
    # MySQL配置
    host = config.get('mysql', 'host')
    port = config.getint('mysql', 'port', fallback=3306)
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    db_name = config.get('mysql', 'db_name')
    
    # 配置数据库URI
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    try:
        db = SQLAlchemy(app)
        with app.app_context():
            db.engine.connect()
        print(f"成功连接到MySQL数据库 {db_name}")
    except (OperationalError, ProgrammingError) as e:
        # 如果数据库不存在，先创建数据库
        if "Unknown database" in str(e):
            print(f"数据库 {db_name} 不存在，尝试创建...")
            try:
                temp_engine = create_engine(
                    f"mysql+pymysql://{user}:{password}@{host}:{port}/mysql?charset=utf8mb4",
                    isolation_level="AUTOCOMMIT"
                )
                
                with temp_engine.connect() as conn:
                    
                    if execute_sql_file('movie_init.sql', conn):
                        print("数据库初始化完成")
                    else:
                        print("数据库初始化失败")
            except Exception as create_error:
                print(f"创建数据库失败: {str(create_error)}")
                exit(1)
        else:
            print(f"无法连接到MySQL服务器: {str(e)}")
            exit(1)
            
elif server_type == 'sqlite':
    # SQLite配置
    filename = config.get('sqlite', 'filename')
    db_path = os.path.join(os.getcwd(), filename)
    app.config["SQLALCHEMY_DATABASE_URI"] = rf"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 检查是否需要初始化
    if not os.path.exists(db_path):
        print("SQLite数据库不存在, 数据库初始化失败")
        exit(1)
    
else:
    print('请填写config.ini选择数据库')
    exit()

def get_db():
    """Get the database instance."""
    return db

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