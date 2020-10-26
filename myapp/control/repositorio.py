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
from myapp.model.entidades import Repositorio

bp = Blueprint("repositorio", __name__, url_prefix="/repositorio")

# Retorna a lista de repositorios do usuario
def lista_repositorios_usuario(id):
    db = get_db()
    query = "select * from repository where user_id = ?"
    repositorios = db.execute( query , (id,) ).fetchall()
    return repositorios

""" Mostra a lista de repositorios  """
@bp.route("/listar")
@login_required
def listar():
    usuario_logado = json.loads(session.get("usuario_logado"))

    # Converte para objeto
    usuario = Usuario( usuario_logado["id"], usuario_logado["name"], usuario_logado["username"], 
            usuario_logado["password"], usuario_logado["image"])

    #Carrega repositorios registrados pelo usuario
    lista_repositorios = lista_repositorios_usuario(usuario_logado["id"])
        
    return render_template("repositorio/listar.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Repositorios", repositorios=lista_repositorios)

""" Mostra a lista de repositorios  """
@bp.route("/listar")
@login_required
def listar_todos():
    usuario_logado = json.loads(session.get("usuario_logado"))

    # Converte para objeto
    usuario = Usuario( usuario_logado["id"], usuario_logado["name"], usuario_logado["username"], 
            usuario_logado["password"], usuario_logado["image"])

    #Carrega usuarios registrados no sistema
    db = get_db()
    query = "SELECT * FROM repository ORDER BY id"
    lista_repositorios = db.execute( query ).fetchall()
        
    return render_template("repositorio/listar.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Repositorios", repositorios=lista_repositorios)

@bp.route("/criar", methods=["GET", "POST"])
@login_required
def criar():
    usuario_logado = json.loads(session.get("usuario_logado"))

    # Converte para objeto
    usuario = Usuario( usuario_logado["id"], usuario_logado["name"], usuario_logado["username"], 
            usuario_logado["password"], usuario_logado["image"])

    """Create a new repository for the current user."""
    if request.method == "POST":
        name = request.form["name"]
        link = request.form["link"]
        error = None

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query_insert = "INSERT INTO repository (name, link, user_id) VALUES (?, ?, ?)"
            db.execute(
                query_insert,(name, link, g.user["id"]),
            )
            db.commit()
            message = "Repositório criado com sucesso!"
            flash(message)
            return redirect(url_for("repositorio.listar"))

    return render_template("repositorio/criar.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Repositorios")

