"""Forms for Flask_Feedback app."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional, Email

class AddUserForm(FlaskForm):
    """User registration form."""

    username=StringField(
        " Username",
        validators=[InputRequired(), Length(min=1, max=20)]
    )

    password = StringField(
        "password",
       validators=[InputRequired(), Length(min=6, max=55)],
    )

    email = StringField(
        "email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    first_name = StringField(
        "first name",
        validators=[InputRequired(), Length( max= 30)],
    )

    last_name = StringField(
        "last name",
        validators=[InputRequired(), Length(max=30)]
    )

# ####################################################################

class Loginform(FlaskForm):
    """Login form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)]
    )

    password = StringField(
        "Password",
        validators= [InputRequired(), Length(min=6, max=55)]
    )




class FeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )


class DeleteForm(FlaskForm):
    """ Delete form -- this form is intentionally blank"""