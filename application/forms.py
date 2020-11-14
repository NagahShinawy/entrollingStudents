from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from . validators import valid_password, valid_email
from .models import User


class LoginForm(FlaskForm):
    # validators=[DataRequired()] ==> means (required Field)
    email = wtforms.StringField(label="Email", validators=[DataRequired(), Email(), valid_email],
                                render_kw={"placeholder": "Type Email"})
    password = wtforms.StringField(label="Password",
                                   validators=[DataRequired(), valid_password, Length(min=6, max=15)],
                                   render_kw={"placeholder": "Type Password", 'type': 'password'})
    remember_me = wtforms.BooleanField(label="Remember Me", default=False)
    submit = wtforms.SubmitField(label="Login", render_kw={'class': 'btn-submit'})


class RegisterForm(FlaskForm):
    # username = wtforms.StringField(label="Username", validators=[DataRequired()])
    email = wtforms.StringField(label="Email", validators=[DataRequired(), Email()],
                                render_kw={"placeholder": "Type Email"})
    fname = wtforms.StringField(label="First Name", validators=[DataRequired(), Length(min=2, max=55)])
    lname = wtforms.StringField(label="Last Name", validators=[DataRequired(), Length(min=2, max=55)])
    password = wtforms.StringField(label="Password",
                                   validators=[DataRequired(), Length(min=6, max=15)],
                                   render_kw={"placeholder": "Type Password", 'type': 'password'})
    password2 = wtforms.StringField(label="Confirm Password", validators=[DataRequired()
        ,Length(min=2, max=55), EqualTo('password')], render_kw={"placeholder": "Type Password", 'type': 'password'})
    submit = wtforms.SubmitField(label="Register")

    def validate_email(self, email):
        email = User.objects.filter(email=email.data).first()
        if email:
            raise ValidationError('Email Already Use')
        return email


