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
from myapp.utils.utilidades import Constant

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
    #Carrega lista de usuarios registrados no sistema
    usuarios = lista_usuarios()
    quantidade_usuarios = len(usuarios)

    #Carregas os repositorios do usuario logado
    repositorios = lista_repositorios_usuario(g.user['id'])
    quantidade_repositorios = len(repositorios)

    return render_template("dashboard/starter.html", usuario = g.user['username'], 
            profilePic=g.user['image'], titulo="Dashboard", usuarios = usuarios, 
            repositorios = repositorios, quantidade_usuarios=quantidade_usuarios, quantidade_repositorios=quantidade_repositorios) 

"""Show the user profile """
@bp.route("/profile")
@login_required
def profile():
    return render_template("dashboard/profile.html", usuario = g.user['username'], 
            profilePic=g.user['image'], titulo="Profile", nome = g.user['name'], id = str(g.user['id']))

@bp.route("/<int:id>/salva", methods=["POST"])
@login_required
def salva(id):
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
            message = "Usuário atualizado com sucesso!"
            flash(message, 'success')

    return redirect(url_for("index"))