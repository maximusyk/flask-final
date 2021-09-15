# region IMPORTS
import json
import math
import os
import secrets
from datetime import datetime, timedelta
from functools import wraps

import jwt
from app.users import users_bp
from flask import abort
from flask import current_app
from flask import current_app as app
from flask import g, redirect, render_template, request, url_for
from flask.json import jsonify
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image, ImageOps

from .forms import *
from .models import *

# endregion


# region CUSTOM_DECS


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("home_bp.index", next=request.url) + "&auth_req")
        return f(*args, **kwargs)

    return decorated_function


def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


# endregion


# region _VARS
menu = [
    ("User", "/register", "user"),
    ("Home", "/", "home"),
    ("About", "/about", "info-circle"),
    ("Portfolio", "/portfolio", "book-content"),
    ("Contact", "/contact", "envelope"),
    ("ToDo List", "/todo", "list-check"),
]
# endregion

# region HELPER FUNS
def save_users(users_db):
    users_list = []

    for user in users_db:
        image_file = url_for("static", filename="img/profile_pics/" + user.image_file)

        last_seen = datetime.strptime(user.last_seen, "%d/%m/%y %H:%M:%S")
        time_now = datetime.now()
        time_sec = (time_now - last_seen).total_seconds()
        last_seen = time_sec / 60
        if last_seen >= 60:
            last_seen = str(math.floor(last_seen / 60)) + "h ago"
        else:
            last_seen = math.floor(last_seen)
            last_seen = str(last_seen) + "m ago"

        role = ""
        actions = ""
        if user.is_admin():
            if user.username == "maksymusyk":
                role = '<span class="role"><span class="status text-danger">&bull;</span> Owner</span>'
            else:
                role = '<span class="role"><span class="status text-warning">&bull;</span> Admin</span>'
        else:
            role = '<span class="role"><span class="status text-success">&bull;</span> User</span>'

        if current_user.username == "maksymusyk":
            actions = f'<a href="#" onclick=admin_update({user.id}) data-toggle="modal" data-target="#userEditModal" class="settings" title="Settings" data-toggle="tooltip"><i class="material-icons">&#xE8B8;</i></a> <a href="#" onclick=admin_delete({user.id}) class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE5C9;</i></a>'
        else:
            if user.username == "maksymusyk":
                actions = f'<a href="#" onclick="access_denied()" class="settings" title="Settings" data-toggle="tooltip"><i class="material-icons">&#xE8B8;</i></a> <a href="#" onclick="access_denied()" class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE5C9;</i></a>'
            else:
                actions = f'<a href="#" onclick=admin_update({user.id}) data-toggle="modal" data-target="#userEditModal" class="settings" title="Settings" data-toggle="tooltip"><i class="material-icons">&#xE8B8;</i></a> <a href="#" onclick=admin_delete({user.id}) class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE5C9;</i></a>'

        users_list.append(
            {
                "id": user.id,
                "name": f'<a href="#" onclick=admin_view({user.id})><img src="{image_file}" class="avatar" alt="Avatar">{user.username}</a>',
                "date_created": user.date_created,
                "last_seen": last_seen,
                "role": role,
                "actions": actions,
            }
        )

    with open("app/static/users.json", "w") as outfile:
        json.dump(users_list, outfile)

    return users_list


def save_picture(form_pictute):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pictute.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/img/profile_pics", picture_fn)

    img = Image.open(form_pictute)
    img_w, img_h = img.size
    if img_w < 500 or img_h < 500:
        if img_w > img_h:
            output_size = (img_h, img_h)
            img = ImageOps.fit(img, output_size, Image.ANTIALIAS)
        else:
            output_size = (img_w, img_w)
            img = ImageOps.fit(img, output_size, Image.ANTIALIAS)
    else:
        output_size = (500, 500)
        img = ImageOps.fit(img, output_size, Image.ANTIALIAS)

    img.save(picture_path)

    return picture_fn


# endregion

# region USERS

# region USER FUNS


@users_bp.route("/user/<int:user_id>/get", methods=["GET", "POST"], endpoint="get_user_info")
@users_bp.route("/admin/render-forms", methods=["GET", "POST"])
@users_bp.route("/admin/user/<int:user_id>/get", methods=["GET", "POST"])
def get_user(user_id=None):
    user = form_edit = form_pass = admin_create_form = admin_update_form = ""
    if request.endpoint == "users_bp.get_user_info":
        user = User.query.get_or_404(user_id)
        form_edit = UserUpdateForm()
        form_pass = ChangePasswordForm()
        return json.dumps(
            {
                "name": user.username,
                "email": user.email,
                "description": user.description,
                "data": render_template(
                    "account_forms.html",
                    mode="user_info",
                    form_edit=form_edit,
                    form_pass=form_pass,
                    req_method=request.method,
                ),
            }
        )
    else:
        admin_create_form = AdminUserCreateForm()
        admin_update_form = AdminUserUpdateForm()
        name = email = admin = ""
        if user_id:
            user = User.query.get_or_404(user_id)
            name = user.username
            email = user.email
            admin = user.admin
        return json.dumps(
            {
                "data": render_template(
                    "account_forms.html",
                    mode="admin_forms",
                    admin_create_form=admin_create_form,
                    admin_update_form=admin_update_form,
                    req_method=request.method,
                ),
                "name": name,
                "email": email,
                "admin": admin,
            }
        )


@users_bp.route("/user_form", methods=["GET"])
def render_auth_form():
    form_in = LoginForm()
    form_up = RegistrationForm()
    if not current_user.is_authenticated:
        return json.dumps(
            {
                "success": "OK",
                "data": render_template(
                    "user_form.html",
                    form_up=form_up,
                    form_in=form_in,
                    req_method=request.method,
                ),
            }
        )
    else:
        return json.dumps({"success": "AUTH"})


@users_bp.route("/signup", methods=["GET", "POST"])
def user_signup():
    form = RegistrationForm()
    users = User.query.all()
    if current_user.is_authenticated:
        return redirect(url_for("home_bp.account"))
    else:
        if form.validate_on_submit():
            usrname = request.form["username"]
            email = request.form["email_up"]
            pwd = request.form["password_up"]
            errors = {}

            for usr in users:
                if usrname == usr.username:
                    errors["username"] = ["Username already taken"]
                else:
                    if "username" in form.errors:
                        errors["username"] = form.errors["username"]

                if email == usr.email:
                    errors["email_up"] = ["Email already taken"]
                else:
                    if "email_up" in form.errors:
                        errors["email_up"] = form.errors["email_up"]

            if "email_up" in errors or "password_up" in errors:
                return json.dumps({"success": "BAD", "errors": "User exist", "data": form.data})

            user = User(username=usrname, email=email, password=pwd)
            try:
                db.session.add(user)
                db.session.commit()

                return json.dumps({"success": "OK", "Title": "User successfuly registered"})
            except Exception as e:
                db.session.rollback()
                json.dump(
                    {
                        "success": "BAD",
                        "Title": "There are some issues adding the user",
                        "errors": e,
                    }
                )
        else:
            # usrname = request.form['username']
            # email = request.form['email_up']
            return json.dumps({"success": "BAD", "data": form.data, "errors": form.errors})


@users_bp.route("/signin", methods=["GET", "POST"])
def user_signin():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("users_bp.account"))
    else:
        # auth = request.authorization

        # user = User.query.filter_by(username=auth.username).first()

        # if user.verify_password(auth.password):
        #     token = jwt.encode(
        #         {"public_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)},
        #         app.config["SECRET_KEY"],
        #         algorithm="HS256",
        #     )
        #     data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        #     print(data)
        #     print(token)
        #     return jsonify({"token": token})

        if form.validate_on_submit():
            email = request.form["email_in"]
            pwd = request.form["password_in"]
            errors = {
                "email_in": "",
                "password_in": "",
            }
            user_db = User.query.filter_by(email=email).first()
            if not user_db:
                user_db = User.query.filter_by(username=email).first()
            if user_db:
                del errors["email_in"]
                if user_db.verify_password(pwd):
                    del errors["password_in"]
                else:
                    errors["password_in"] = ["Wrong password"]
            else:
                errors["email_in"] = ["Username or email not found"]
                errors["password_in"] = ["Wrong password"]

            if "email_in" in errors or "password_in" in errors:
                return json.dumps({"success": "BAD", "errors": errors, "data": form.data})

            login_user(user_db, remember=form.remember_me.data)
            user_db.last_seen = datetime.now().strftime("%d/%m/%y %H:%M:%S")
            db.session.commit()
            # TODO move nav menu to helpers
            return json.dumps({"success": "OK", "data": render_template("nav_menu.html", menu=menu)})
        else:
            email = request.form["email_in"]
            pwd = request.form["password_in"]
            errors = {
                "email_in": "",
                "password_in": "",
            }
            user_db = User.query.filter_by(email=email).first()
            if not user_db:
                user_db = User.query.filter_by(username=email).first()
            if user_db:
                del errors["email_in"]
                if user_db.verify_password(pwd):
                    del errors["password_in"]
                else:
                    errors["password_in"] = ["Wrong password"]
            else:
                errors["email_in"] = ["Username or email not found"]
                errors["password_in"] = ["Wrong password"]

            if "email_in" in errors or "password_in" in errors:
                return json.dumps({"success": "BAD", "errors": errors, "data": form.data})
            return json.dumps({"success": "BAD", "data": form.data, "errors": form.errors})


@users_bp.route("/user/<int:user_id>/password/change", methods=["GET", "POST"])
@auth_required
def user_change_pwd(user_id):
    form = ChangePasswordForm
    user = User.query.get_or_404(user_id)
    if form.validate_on_submit() and request.method == "POST":
        old_pwd = request.form["old_pwd"]
        if not user.verify_password(old_pwd):
            form.errors["old_pwd"] = ["Wrong password"]
            return json.dumps({"success": "BAD", "errors": form.errors, "data": form.data})

        current_user.password = pbkdf2_sha256.hash(request.form["new_pwd"])
        db.session.commit()

        return json.dumps({"success": "OK"})
    else:
        old_pwd = request.form["old_pwd"]
        errors = form.errors
        if not user.verify_password(old_pwd):
            print("=====")
            errors["old_pwd"] = ["Wrong password"]
        print(errors)

        return json.dumps({"success": "BAD", "data": form.data, "errors": errors})


@users_bp.route("/user/<int:user_id>/edit", methods=["GET", "POST"])
@auth_required
def user_info_edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserUpdateForm()
    if form.validate_on_submit() and request.method == "POST":
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file

        user.username = request.form["username"]
        user.email = request.form["email"]
        user.description = request.form["description"]
        db.session.commit()

        return json.dumps({"success": "OK", "Title": "User info successfuly updated"})

    else:
        response_data = {k: form.data[k] for k in form.data.keys() - {"picture"}}
        return json.dumps({"success": "BAD", "data": response_data, "errors": form.errors})


@users_bp.route("/logout", methods=["GET"])
@auth_required
def logout():
    logout_user()
    return redirect(url_for("home_bp.index"))


@users_bp.route("/account", methods=["GET"])
@auth_required
def account():
    image_file = url_for("static", filename="img/profile_pics/" + current_user.image_file)

    last_seen = datetime.strptime(current_user.last_seen, "%d/%m/%y %H:%M:%S")
    time_now = datetime.now()
    time_sec = (time_now - last_seen).total_seconds()
    last_seen = time_sec / 60
    if last_seen >= 60:
        last_seen = str(math.floor(last_seen / 60)) + "h ago"
    else:
        last_seen = math.floor(last_seen)
        if last_seen <= 5:
            last_seen = "recently"
        else:
            last_seen = str(last_seen) + "m ago"

    if current_user.is_admin():
        return admin_list(last_seen, image_file)

    return render_template("account.html", menu=menu, last_seen=last_seen, image_file=image_file)


# endregion

# region ADMIN FUNS


def admin_list(last_seen, image_file):

    save_users(User.query.all())

    return render_template("account.html", menu=menu, last_seen=last_seen, image_file=image_file)


@users_bp.route("/admin/create/user", methods=["GET", "POST"])
@auth_required
@admin_login_required
def user_create_admin():
    form = AdminUserCreateForm()
    users = User.query.all()
    if form.validate_on_submit():
        username = request.form["username_admin_create"]
        email = request.form["email_admin_create"]
        pwd = request.form["password_admin_create"]

        # TODO
        is_admin_create = form.is_admin_create.data

        print("is_admin_create")
        print(is_admin_create)
        print("is_admin_create")
        # TODO

        errors = {}

        for usr in users:
            if username == usr.username:
                print("\n\nUsername already taken")
                errors["username_admin_create"] = ["Username already taken"]
            else:
                if "username" in form.errors:
                    print("\n\nUsername already taken")
                    errors["username_admin_create"] = form.errors["username_admin_create"]

            if email == usr.email:
                print("\n\nUsername already taken")
                errors["email_admin_create"] = ["Email already taken"]
            else:
                if "email_up" in form.errors:
                    errors["email_admin_create"] = form.errors["email_admin_create"]

        if "username_admin_create" in errors or "email_admin_create" in errors or "password_admin_create" in errors:
            return json.dumps({"success": "BAD", "errors": "User exist", "data": form.data})

        user = User(username=username, email=email, password=pwd, admin=is_admin_create)
        try:
            db.session.add(user)
            db.session.commit()

            return json.dumps({"success": "OK", "data": save_users(User.query.all())})
        except Exception as e:
            json.dump(
                {
                    "success": "BAD",
                    "Title": "There are some issues adding the user",
                    "errors": e,
                }
            )
    else:
        return json.dumps({"success": "BAD", "data": form.data, "errors": form.errors})

    return json.dumps(
        {"data": render_template("account_forms.html", admin_create_form=form, req_method=request.method)}
    )


@users_bp.route("/admin/update/user/<int:user_id>", methods=["GET", "POST"])
@auth_required
@admin_login_required
def user_update_admin(user_id):
    form = AdminUserUpdateForm()
    user = User.query.get_or_404(user_id)
    users = User.query.all()
    if form.validate_on_submit() and request.method == "POST":
        username = request.form["username_admin_update"]
        email = request.form["email_admin_update"]

        # TODO
        user.admin = form.is_admin_update.data
        # TODO

        errors = {}
        print("\n\n*** Validation-1 ***\n")
        for usr in users:
            if username != user.username:
                if username == usr.username:
                    print("\n\nUsername already taken")
                    errors["username_admin_update"] = ["Username already taken"]
                else:
                    if "username_admin_update" in form.errors:
                        print("\n\nUsername already taken")
                        errors["username_admin_update"] = form.errors["username_admin_update"]

            if email != user.email:
                if email == usr.email:
                    print("\n\nUsername already taken")
                    errors["email_admin_update"] = ["Email already taken"]
                else:
                    if "email_admin_update" in form.errors:
                        errors["email_admin_update"] = form.errors["email_admin_update"]

        print(errors)

        if "username_admin_update" in errors or "email_admin_update" in errors or "password_up" in errors:
            return json.dumps({"success": "BAD", "errors": errors, "data": form.data})

        print("\n*** End Validation-1 ***\n\n")

        user.username = username
        user.email = email

        db.session.commit()

        return json.dumps({"success": "OK", "data": save_users(User.query.all())})

    else:
        username = request.form["username_admin_update"]
        email = request.form["email_admin_update"]

        errors = {}
        print("\n\n*** Validation-2 ***\n")
        for usr in users:
            if username == usr.username:
                print("\n\nUsername already taken")
                errors["username_admin_update"] = ["Username already taken"]
            else:
                if "username_admin_update" in form.errors:
                    print("\n\nUsername already taken")
                    errors["username_admin_update"] = form.errors["username_admin_update"]

            if email == usr.email:
                print("\n\nUsername already taken")
                errors["email_admin_update"] = ["Email already taken"]
            else:
                if "email_admin_update" in form.errors:
                    errors["email_admin_update"] = form.errors["email_admin_update"]

        if "username" in errors or "email_admin_update" in errors or "password_up" in errors:
            return json.dumps({"success": "BAD", "errors": "User exist", "data": form.data})

        print("\n*** End Validation-2 ***\n\n")

        return json.dumps({"success": "BAD", "errors": form.errors})


@users_bp.route("/admin/view/user/<int:user_id>", methods=["GET", "POST"])
@auth_required
@admin_login_required
def user_view_admin(user_id):
    user = User.query.get_or_404(user_id)
    image_file = url_for("static", filename="img/profile_pics/" + user.image_file)

    last_seen = datetime.strptime(user.last_seen, "%d/%m/%y %H:%M:%S")
    time_now = datetime.now()
    time_sec = (time_now - last_seen).total_seconds()
    last_seen = time_sec / 60
    if last_seen >= 60:
        last_seen = str(math.floor(last_seen / 60)) + "h ago"
    else:
        last_seen = math.floor(last_seen)
        if last_seen <= 5:
            last_seen = "recently"
        else:
            last_seen = str(last_seen) + "m ago"

    return json.dumps(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "last_seen": last_seen,
            "description": user.description,
            "image": image_file,
        }
    )


@users_bp.route("/admin/delete/user/<int:user_id>")
@auth_required
@admin_login_required
def user_delete_admin(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return json.dumps({"success": "OK", "data": save_users(User.query.all())})
    except:
        return json.dumps({"success": "BAD"})
    return redirect(url_for(".home_admin"))


# endregion


@users_bp.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        db.session.commit()
    return response


# endregion
