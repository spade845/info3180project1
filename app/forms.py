from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired, Required
from flask_wtf.file import FileField, FileAllowed, FileRequired 

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
    
class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    age = IntegerField('Age', validators=[Required()])
    gender = SelectField('Gender', choices=[('Male','Male'), ('Female', 'Female')], validators=[Required()])
    bio = StringField('Bio', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    image = FileField('Image',validators = [FileRequired(),FileAllowed(['jpg, png'])])
    
    