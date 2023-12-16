from wtforms import StringField
from wtforms.validators import Length,InputRequired
from flask_wtf import FlaskForm

class SQLServerForm(FlaskForm):
    server = StringField('Server', default='DESKTOP-4KEIUAR', validators=[InputRequired(), Length(max=50)])
    user = StringField('User', default='sa', validators=[InputRequired(), Length(max=50)])
    password = StringField('Password', default='123456', validators=[InputRequired(), Length(max=50)])
    database = StringField('Database', default='movieDBtest', validators=[InputRequired(), Length(max=50)])

class SQLiteForm(FlaskForm):
    file_path = StringField('File_PAth', default='movieDB.db', validators=[InputRequired()])