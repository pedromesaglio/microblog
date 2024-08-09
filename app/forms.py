from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _1
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa 
from app import db 
from app.models import User 
from wtforms import TextAreaField 
from wtforms.validators import Length



class LoginForm(FlaskForm):
    username = StringField(_1('Username', validators=[DataRequired()]))
    password = PasswordField(_1('Password', validators=[DataRequired()]))
    remember_me = BooleanField(_1('Remember Me'))
    submit = SubmitField(_1('Sing In'))
    
class RegistrationForm(FlaskForm):
    username = StringField(_1('Username', validators=[DataRequired()]))
    email = StringField(_1('Email', validators=[DataRequired(), Email()]))
    password = PasswordField(_1('Password', validators=[DataRequired()]))
    password2 = PasswordField(_1('Repeat Password', validators=[DataRequired(), EqualTo('password')]))
    submit = SubmitField(_1('Register'))
    
def validate_username(self, username):
    user = db.session.scalar(sa.select(User).where(User.username == username.data))
    if user is not None:
        raise ValidationError(_('Please use a different username.'))
    
def validate_email(self, email):
    user = db.session.scalar(sa.select(User).where(User.email == email.data))
    if user is not None:
        raise ValidationError(_('Please use a different email adress.'))
    
class EditProfileForm(FlaskForm):
    username = StringField(_1('Username', validators=[DataRequired()]))
    about_me = TextAreaField(_1('About Me', validators=[Length(min=0, max=140)]))
    submit = SubmitField(_1('Submit'))
    
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
    
class PostForm(FlaskForm):
    post = TextAreaField(_1('Say something', validators=[DataRequired(), Length(min=1, max=140)]))
    submit = SubmitField(_1('Submit'))
    
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_1('Email', validators=[DataRequired(), Email()]))
    submit = SubmitField(_1('Request Password Reset'))
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField(_1('Password', validators=[DataRequired()]))
    password2 = PasswordField(_1('Repeat Password', validators=[DataRequired(), EqualTo('password')]))
    submit = SubmitField(_1('Request Password Reset'))
    