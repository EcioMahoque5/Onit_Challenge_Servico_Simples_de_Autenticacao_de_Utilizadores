from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

class UserRegistrationForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message="username is a required field!"), 
        Length(min=4, max=32,message="Username must have 4-32 characters!")])
    
    password = PasswordField('password', validators=[
        DataRequired(message="password is a required field!"),
        Regexp(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_+-=]).{8,32}$',
                message='Password must include at least one uppercase letter, one lowercase letter, one number, and one special character, and be between 8 and 32 characters long'
        )
    ])
        
        
class LoginForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message="username is a required field!")])
    
    password = PasswordField('password', validators=[
        DataRequired(message="password is a required field!")])
    
class LogoutForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(message="username is a required field!")])