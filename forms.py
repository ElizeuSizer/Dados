from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=150)])
    submit = SubmitField("Registrar")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=150)])
    submit = SubmitField("Entrar")
