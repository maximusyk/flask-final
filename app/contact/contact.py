# region _IMPORTS

import json

from app.contact import contact_bp
from flask import flash, redirect, render_template, request, session, url_for

from .forms import *

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


def writeJSON(data, filename="dump.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# region _ROUTES
@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST":
        if "name" in session and "email" in session:
            print(
                f"\n<<=== EXISTED VALUES ===>>Name -> {session.get('name')}\nEmail -> {session.get('email')}")
            form.name.data = session.get("name")
            form.email.data = session.get("email")
            if form.validate_on_submit():
                sbj = request.form["subject"]
                msg = request.form["message"]
                with open("dump.json") as jsonFile:
                    data = json.load(jsonFile)
                    temp = data["usrMessages"]
                    temp.append(
                        {
                            "Name": form.name.data,
                            "Email": form.email.data,
                            "Subject": form.subject.data,
                            "Message": form.message.data,
                        }
                    )
                writeJSON(data)
                flash("Your message has been sent. Thank you!", "message")
                return redirect(url_for("contact"))
            else:
                flash("There were some issues sending the message!", "error")
        else:
            if form.validate_on_submit():
                usrName = form.name.data
                usrEmail = form.email.data
                sbj = form.subject.data
                msg = form.message.data
                session["name"] = usrName
                session["email"] = usrEmail
                with open("dump.json") as jsonFile:
                    data = json.load(jsonFile)
                    temp = data["usrMessages"]
                    temp.append(
                        {
                            "Name": form.name.data,
                            "Email": form.email.data,
                            "Subject": form.subject.data,
                            "Message": form.message.data,
                        }
                    )
                writeJSON(data)
                flash("Your message has been sent. Thank you!", "message")
                return redirect(url_for("contact"))
            else:
                flash("There were some issues sending the message!", "error")

    # return "Hello"
    return render_template(
        "contact.html",
        menu=menu,
        form=form,
        reqMethod=request.method,
    )
# endregion
