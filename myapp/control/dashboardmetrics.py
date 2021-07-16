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

bp = Blueprint("dashboardmetrics", __name__)

# Retorna a lista de repositorios do usuario
def lista_repositorios_usuario(id):
    db = get_db()
    query = "select * from repository where user_id = ?"
    repositorios = db.execute( query , (id,) ).fetchall()
    return repositorios

"""Show the user dashboard """
@bp.route("/metrics")
@login_required
def index():
    #Carregas os repositorios do usuario logado
    repositorios = lista_repositorios_usuario(g.user['id'])
    quantidade_repositorios = len(repositorios)

    return render_template("dashboardmetrics/starter.html", usuario = g.user['username'],profilePic=g.user['image'], 
        titulo="DashboardMetrics", repositorios = repositorios, quantidade_repositorios=quantidade_repositorios) 