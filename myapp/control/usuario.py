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

bp = Blueprint("usuario", __name__, url_prefix="/usuario")

""" Mostra a lista de usuarios  """
@bp.route("/listar")
@login_required
def listar():
    usuario_logado = json.loads(session.get("usuario_logado"))

    # Converte para objeto
    usuario = Usuario( usuario_logado["id"], usuario_logado["name"], usuario_logado["username"], 
            usuario_logado["password"], usuario_logado["image"])

    #Carrega usuarios registrados no sistema
    db = get_db()
    query = "SELECT * FROM user ORDER BY id"
    lista_usuarios = db.execute( query ).fetchall()
        
    return render_template("usuario/listar.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Usuários", usuarios=lista_usuarios)