from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask import session

from myapp.control.auth import login_required
from myapp.config.db import get_db
import json
from myapp.model.entidades import Usuario

bp = Blueprint("dashboard", __name__)

"""Show the user dashboard """
@bp.route("/")
@login_required
def index():
    # usuario_logado carrega uma estrutura de dicionario
    usuario_logado = json.loads(session.get("usuario_logado"))

    # Converte para objeto
    usuario = Usuario( usuario_logado["id"], usuario_logado["name"], usuario_logado["username"], 
            usuario_logado["password"], usuario_logado["image"])

    #Carrega lista de usuarios registrados no sistema
    #Carregas as notas do usuario logado
    return render_template("dashboard/starter.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Starter Page")

def get_usuario(id):
    id = int(id)
    query = "SELECT * FROM user WHERE id = ?"
    user = get_db().execute( query , (id,) ).fetchone()

    if user is None:
        abort(404, "User id {0} doesn't exist.".format(id))

    return user

"""Show the user profile """
@bp.route("/profile")
@login_required
def profile():
    usuario_id = json.loads(session.get("usuario_logado"))
    # Pega os dados atualizados do usuario logado
    usuario_logado = get_usuario(usuario_id["id"])

    # Converte para objeto
    usuario = Usuario( usuario_logado["id"], usuario_logado["name"], usuario_logado["username"], 
            usuario_logado["password"], usuario_logado["image"])

    return render_template("dashboard/profile.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Profile", nome = usuario.name, id = str(usuario.id))

@bp.route("/<int:id>/salva", methods=["POST"])
@login_required
def salva(id):
    usuario_logado = json.loads(session.get("usuario_logado"))

    if request.method == "POST": 
        # Carrega dados do formulario
        name = request.form["name"]
        username = request.form["email"]
        error = None

        if not username:
            error="Username is required"

        if error is not None:
            flash(error)
        else:
            # Faz o updade no banco 
            db = get_db()
            query = "Update user set name = ?, username = ? where id = ?"
            db.execute( query, (name, username, id) ) 
            db.commit()

    return redirect(url_for("index"))