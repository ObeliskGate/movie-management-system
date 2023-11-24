from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

db_name = 'movieDB'
app.config["SQLALCHEMY_DATABASE_URI"] = f'mssql+pymssql://sa:123456@DESKTOP-4KEIUAR/{db_name}?charset=utf8'

app.config['SECRET_KEY'] = 'secret_key'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
from src import routes

def db_connect_check():
    '''
    check whether to connect movieDB from SQL server'''
    with app.app_context():
        try:
            db.engine.connect()
            print("Successfully connected to the database")
            return True
        except OperationalError as e:
            print("Fail to connect to database")
            print(e.orig.args[0][1].decode('utf-8'))
            return False
