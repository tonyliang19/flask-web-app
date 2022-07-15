# Contains WTF Forms to be submitted by users, uses csrs token to secure it
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User
# For login
class LoginForm(FlaskForm):
    # Add validators to state some field is REQUIRED to submit
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    # Check box for "Remember me", uses Boolean Field 
    remember_me = BooleanField("Remember Me")
    # submit button, usually bind to a function, where we call it later
    submit = SubmitField("Login")

# For user to register
class RegisterForm(FlaskForm):
    # Add validators to state some field is REQUIRED to submit
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    # EqualTo requires it to match the variable "password"
    password_confirm = PasswordField("Confirm Password", 
                                    validators=[DataRequired(),
                                    Length(min=6, max=15),EqualTo("password")])
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=55)])
    submit = SubmitField("Register Now")

    # Note the function name validate_xxx , xxx must match EXACT case of the variable defined earlier
    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")
