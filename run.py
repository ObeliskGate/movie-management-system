from src import app, db_connect_check

if __name__ == '__main__':
    if db_connect_check():
        app.run(debug=True)