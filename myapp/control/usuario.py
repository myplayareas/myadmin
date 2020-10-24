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

bp = Blueprint("usuario", __name__, url_prefix="/usuario")

""" Mostra a lista de usuarios  """
@bp.route("/listar")
@login_required
def listar():
    usuario_logado = json.loads(session.get("usuario_logado"))
        
    #Carrega usuarios registrados no sistema
    db = get_db()
    lista_usuarios = db.execute(
            'SELECT *'
            ' FROM user'
            ' ORDER BY id'
    ).fetchall()
        
    return render_template("usuario/listar.html", usuario = usuario_logado["username"], 
            profilePic=usuario_logado["imagem"], titulo="Lista de Usuários", usuarios=lista_usuarios)