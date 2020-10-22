from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask import session

from myapp.auth import login_required
from myapp.db import get_db
import json

bp = Blueprint("dashboard", __name__)

"""Show the user dashboard """
@bp.route("/")
def index():
    if session.get("usuario_logado") is not None:
        usuario_logado = json.loads(session.get("usuario_logado"))
        return render_template("dashboard/starter.html", usuario = usuario_logado["username"], profilePic=usuario_logado["imagem"], titulo="Starter Page")
    return redirect(url_for("auth.login"))

"""Show the user profile """
@bp.route("/profile")
def profile():
    if session.get("usuario_logado") is not None:
        usuario_logado = json.loads(session.get("usuario_logado"))
        return render_template("dashboard/profile.html", usuario = usuario_logado["username"], profilePic=usuario_logado["imagem"], titulo="Profile")
    return redirect(url_for("auth.login"))
