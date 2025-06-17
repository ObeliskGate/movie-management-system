from src.server import app, db_connect_check

if __name__ == '__main__':
    db_connect_check()   
    app.run(port=12345, debug=True)