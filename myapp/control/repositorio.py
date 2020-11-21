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

import datetime
from myapp.services.check_commits import CheckCommits
import numpy as np
from os import path
import matplotlib.pyplot as plt
from myapp.utils.utilidades import Util
from threading import Thread

bp = Blueprint("repositorio", __name__, url_prefix="/repositorio")

# Faz o processamento da analise do repositorio
def processing(repository, name):
    try:
        # Class that represents a repository analysis
        analysis = CheckCommits(repository, name)

        print("SysRepo Analysis - v: 1.0.0", datetime.datetime.now())
        print("Repository: ", repository)

        before1 = datetime.datetime.now()
        print("Started on: ", before1)
        print("Please wait...")

        frequencyOfEachFile = None

        try: 
            print("Processing the frequency of each file in commits...")
            frequencyOfEachFile = analysis.counterWithFrequencyOfFile()
            print(frequencyOfEachFile)
        except:
            print("Error in analysis.counterWithFrequencyOfFile()")

        try: 
            # Save frequencyOfEachFile in a json file
            singleName = name + ".json"
            JSON_PATH = '/Users/armandosoaressousa/git/myadmin/myapp/static' + "/json"
            path_to_save = JSON_PATH + "/"
            fileName = path_to_save + name + ".json"
            with open(fileName, 'w', encoding="utf-8") as jsonFile:
                json.dump(frequencyOfEachFile, jsonFile)
            print("The file {} was saved with success!".format( singleName ))
        except: 
            print( "Error when try to save the json file")

        print( "Processing word cloud...")
        analysis.generateWordCloud()

        after =  datetime.datetime.now()
        print("The wordcloud was generated with success!")
        print("Finished on: ", after)
    except:
        print("Something wrong!")
    finally:
        print("Finished processing!")
    return frequencyOfEachFile

# Retorna a lista de repositorios do usuario
def lista_repositorios_usuario(id):
    db = get_db()
    query = "select * from repository where user_id = ?"
    repositorios = db.execute( query , (id,) ).fetchall()
    return repositorios

# Retorna os dados de um repositorio especifico
def dados_do_repositorio(id):
    db = get_db()
    query = "select * from repository where id = ?"
    repositorio = db.execute( query, (id,) ).fetchone()      
    return repositorio

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
        
# Visualiza as informacoes de um dado repositorio selecionado
@bp.route("/<int:id>/visualizar", methods=["GET"])
@login_required
def visualizar(id):
    usuario_logado = json.loads(session.get("usuario_logado"))
    # Converte para objeto
    usuario = Usuario( usuario_logado["id"], usuario_logado["name"], usuario_logado["username"], 
            usuario_logado["password"], usuario_logado["image"])
    
    # Dados do reposotorio
    repositorio = dados_do_repositorio(id)
    link = repositorio['link']
    name = repositorio['name']
    
    # Metricas do repositorio
    # Processa o repositorio para gerar a lista dos arquivos mais modificados
    # Processa o repositorio para gerar a nuvem de arquivos mais modificados
    arquivos = processing(link, name)

    return render_template("repositorio/visualizar.html", usuario = usuario.username, 
            profilePic=usuario.image, titulo="Detalhes do Repositorio", name=name, arquivos=arquivos)