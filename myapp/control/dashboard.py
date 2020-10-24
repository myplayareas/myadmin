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
import os

bp = Blueprint("dashboard", __name__)

"""Show the user dashboard """
@bp.route("/")
@login_required
def index():
    # usuario_logado carrega uma estrutura de dicionario
    usuario_id = json.loads(session.get("usuario_logado"))
    # Pega os dados atualizados do usuario logado
    usuario_logado = get_usuario(usuario_id["id"])

    # Converte para objeto
    usuario = Usuario( usuario_logado["id"], usuario_logado["name"], usuario_logado["username"], 
            usuario_logado["password"], usuario_logado["image"])

    #Carrega lista de usuarios registrados no sistema
    #Carregas as notas do usuario logado
    return render_template("dashboard/starter.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Dashboard")

# Dado um id de usuario retorna um user (dicionario)
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
    if request.method == "POST": 
        # Carrega dados do formulario
        name = request.form["name"]
        username = request.form["email"]

        file_image = request.files["arquivo"]
        file_name_to_store = "picture-" + str(id) + ".png"
        UPLOAD_PATH = '/Users/armandosoaressousa/git/myadmin/myapp/static' + '/uploads'
        path_to_save = UPLOAD_PATH + "/" + file_name_to_store

        error = None

        if not username:
            error="Username is required"

        if error is not None:
            flash(error)
        else:
            # Salva o arquivo no diretorio de uploads
            file_image.save(path_to_save)

            # Faz o updade no banco 
            db = get_db()
            query = "Update user set name = ?, username = ?, image = ? where id = ?"
            db.execute( query, (name, username, file_name_to_store, id) ) 
            db.commit()

    return redirect(url_for("index"))