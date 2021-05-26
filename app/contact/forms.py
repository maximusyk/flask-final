from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

csrf = CSRFProtect()


class ContactForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(message="Name cannot be empty")]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="E-mail cannot be empty"),
            Email("Enter a valid email(abc@example.xyz)"),
        ],
    )
    subject = StringField(
        "Subject", validators=[DataRequired(message="Subject cannot be empty")]
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Message cannot be empty"),
            Length(min=2, max=100),
        ],
    )
