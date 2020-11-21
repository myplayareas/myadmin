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

# Retorna a lista de usuarios
def lista_usuarios():
    db = get_db()
    query = "select * from user"
    usuarios = db.execute(query).fetchall()
    return usuarios

# Retorna a lista de repositorios do usuario
def lista_repositorios_usuario(id):
    db = get_db()
    query = "select * from repository where user_id = ?"
    repositorios = db.execute( query , (id,) ).fetchall()
    return repositorios

"""Show the user dashboard """
@bp.route("/")
@login_required
def index():
    # usuario_id carrega uma estrutura de dicionario
    usuario_id = json.loads(session.get("usuario_logado"))
    # Pega os dados atualizados do usuario logado
    usuario = get_usuario(usuario_id["id"])

    #Carrega lista de usuarios registrados no sistema
    usuarios = lista_usuarios()

    quantidade_usuarios = len(usuarios)

    #Carregas os repositorios do usuario logado
    repositorios = lista_repositorios_usuario(usuario.id)
    print(repositorios)

    return render_template("dashboard/starter.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Dashboard", usuarios = usuarios, 
            repositorios = repositorios, quantidade_usuarios=quantidade_usuarios) 

# Dado um id de usuario retorna um usuario (objeto)
def get_usuario(id):
    id = int(id)
    query = "SELECT * FROM user WHERE id = ?"
    user = get_db().execute( query , (id,) ).fetchone()

    if user is None:
        abort(404, "User id {0} doesn't exist.".format(id))

    # Converte para objeto
    usuario = Usuario( user["id"], user["name"], user["username"], user["password"], user["image"])

    return usuario

"""Show the user profile """
@bp.route("/profile")
@login_required
def profile():
    usuario_id = json.loads(session.get("usuario_logado"))
    # Pega os dados atualizados do usuario logado
    usuario = get_usuario(usuario_id["id"])

    return render_template("dashboard/profile.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Profile", nome = usuario.name, id = str(usuario.id))

@bp.route("/<int:id>/salva", methods=["POST"])
@login_required
def salva(id):
    if request.method == "POST": 
        # Carrega dados do formulario
        name = request.form["name"]
        username = request.form["email"]

        # TO DO: isolar o tratamento de arquivo
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
            message = "Usuário atualizado com sucesso!"
            flash(message)

    return redirect(url_for("index"))