from app.users.users import admin_login_required
from .forms import *
from flask import flash, redirect, request, url_for
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_login import current_user, login_required
from passlib.hash import pbkdf2_sha256
from wtforms import PasswordField, StringField, TextAreaField, widgets
from wtforms.validators import DataRequired, Email, Length


class CustomView(BaseView):
    @expose("/")
    @login_required
    @admin_login_required
    def index(self):
        return self.render("admin/custom.html")

    @expose("/second_page")
    @login_required
    @admin_login_required
    def second_page(self):
        return self.render( "admin/second_page.html")


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class UserAdminView(ModelView):
    column_searchable_list =("username",)
    column_sortable_list = ("username", "admin")
    column_exclude_list = ("password",)
    form_excluded_columns = ("password",)
    form_edit_rules = ("username", "admin")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField("Password")
        form_class.new_password = PasswordField("New Password")
        form_class.confirm = PasswordField("Confirm New Password")

        return form_class

    def create_model(self, form):
        model = self.model(
            form.username.data,
            form.email.data,
            pbkdf2_sha256.hash(form.password.data),
            form.description.data,
            form.admin.data,
        )
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()

    form_edit_rules = ("username", "email", "admin", rules.Header("Reset Password"), "new_password", "confirm")
    form_create_rules = ("username", "email","description", "password", "admin")

    form_overrides = dict(description=CKTextAreaField)

    create_template = 'admin/create.html'

    def update_model(self, form, model):
        form.populate_obj(model)
        if form.new_password.data:
            if form.new_password.data != form.confirm.data:
                flash("Passwords must match")
            model.password = pbkdf2_sha256.hash(form.new_password.data)

        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, *kwargs):
        return redirect(url_for("index", next=request.url))
