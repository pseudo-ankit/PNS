from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from NewsApp.models import UserDetails
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                        validators = [DataRequired(), EqualTo('password')])

    business = IntegerRangeField('Business', default=1, validators = [DataRequired()])
    entertainment = IntegerRangeField('Entertainment', default=1, validators = [DataRequired()])
    health = IntegerRangeField('Health', default=1, validators = [DataRequired()])
    science = IntegerRangeField('Science', default=1, validators = [DataRequired()])
    sports = IntegerRangeField('Sports', default=1, validators = [DataRequired()])
    technology = IntegerRangeField('Technology', default=1, validators = [DataRequired()])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = UserDetails.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = UserDetails.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):

    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    profile_pic = FileField('Update Profle Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def validate_username(self, username):
        if current_user.username != username.data:
            user = UserDetails.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists!')

    def validate_email(self, email):
        if current_user.email != email.data:
            email = UserDetails.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already exists!')
