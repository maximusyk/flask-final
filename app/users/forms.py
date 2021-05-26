from flask_login import current_user
from flask_wtf import CSRFProtect, FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError

from .models import User

csrf = CSRFProtect()


class RegistrationForm(FlaskForm):
    username = StringField(
        "username",
        validators=[
            Length(min=4, max=25, message="Username must contain 4-25 characters"),
            DataRequired(message="This field cannot be empty"),
        ],
    )
    email_up = StringField("email_up", validators=[DataRequired(message="Email cannot be empty"), Email()])
    password_up = PasswordField(
        "password_up",
        validators=[
            Length(min=6, message="The password cannot be less than 6 characters"),
            DataRequired(message="Password cannot be empty"),
        ],
    )
    confirm_password = PasswordField(
        "conf_password",
        validators=[
            DataRequired(message="Passwords must match."),
            EqualTo("password_up", message="Passwords must match."),
        ],
    )

    def validate_email_up(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already taken")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken")


class LoginForm(FlaskForm):
    email_in = StringField("email_in", validators=[DataRequired(message="Username cannot be empty")])
    password_in = PasswordField("password_in", validators=[DataRequired(message="Password cannot be empty")])
    remember_me = BooleanField("remember_me")


class UserUpdateForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField("email", validators=[DataRequired(), Email()])

    description = TextAreaField(
        "description",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
        render_kw={"rows": 3},
    )

    picture = FileField("Update Profile Photo", render_kw={"accept": "image/*"})

    def validate_username(self, field):
        if field.data != current_user.username:
            username = User.query.filter_by(username=field.data).first()
            if username:
                raise ValidationError("Username already taken. Please choose a different one.")

    def validate_email(self, field):
        if field.data != current_user.email:
            email = User.query.filter_by(email=field.data).first()
            if email:
                raise ValidationError("Email already taken. Please choose a different one.")


class ChangePasswordForm(FlaskForm):
    old_pwd = PasswordField("old_pwd", validators=[DataRequired(message="Password cannot be empty")])

    new_pwd = PasswordField(
        "new_pwd",
        validators=[
            Length(min=6, message="The password cannot be less than 6 characters"),
            DataRequired(message="Password cannot be empty"),
        ],
    )

    con_pwd = PasswordField(
        "con_pwd",
        validators=[DataRequired(message="Passwords must match."), EqualTo("new_pwd", message="Passwords must match.")],
    )


class AdminUserCreateForm(FlaskForm):
    username_admin_create = StringField(
        "username_admin_create",
        validators=[
            Length(min=4, max=25, message="Username must contain 4-25 characters"),
            DataRequired(message="This field cannot be empty"),
        ],
    )
    email_admin_create = StringField(
        "email_admin_create", validators=[DataRequired(message="Email cannot be empty"), Email()]
    )
    password_admin_create = PasswordField(
        "password_admin_create",
        validators=[
            Length(min=6, message="The password cannot be less than 6 characters"),
            DataRequired(message="Password cannot be empty"),
        ],
    )
    is_admin_create = BooleanField("is_admin_create")

    def validate_email_admin_create(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already taken")

    def validate_username_admin_create(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken")


class AdminUserUpdateForm(FlaskForm):
    username_admin_update = StringField(
        "username_admin_update",
        validators=[
            Length(min=4, max=25, message="Username must contain 4-25 characters"),
            DataRequired(message="This field cannot be empty"),
        ],
    )
    email_admin_update = StringField(
        "email_admin_update", validators=[DataRequired(message="Email cannot be empty"), Email()]
    )
    is_admin_update = BooleanField("is_admin_update")

    # def validate_email_admin_update(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError("Email already taken")

    # def validate_username_admin_update(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError("Username already taken")
