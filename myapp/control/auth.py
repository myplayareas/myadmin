import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from myapp.config.db import get_db
from myapp.model.entidades import Usuario
from myapp.utils.utilidades import MyEncoder

bp = Blueprint("auth", __name__)

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = ( get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone() )

# Pagina de registro
@bp.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register a new user.
    Validates that the username is not already taken. Hashes the password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        email = request.form["username"]

        db = get_db()
        query = "SELECT id FROM user WHERE username = ?"
        query_insert = "INSERT INTO user (username, password, name, image, email) VALUES (?, ?, ?, ?, ?)"
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (    
            db.execute(query, (username,)).fetchone()
            is not None
        ):
            error = f"User {username} is already registered."

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                query_insert,
                (username, generate_password_hash(password), name, 'anonymous2.png', email),
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        query = "SELECT * FROM user WHERE username = ?"
        error = None

        user = db.execute( query, (username,) ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            # No caso do flask e preciso fazer o encode de um objeto para um json
            # Obs: no Flask as sessoes guardam uma estrutura de dicionario
            session["usuario_logado"] = MyEncoder().encode(Usuario(user["id"], user["name"], user["username"], user["password"], user["image"]))
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return render_template("auth/login.html")

# Pagina de recuperacao de e-mail
@bp.route("/forgot-password", methods=["GET"])
def forgot():
    return render_template("auth/forgot-password.html")