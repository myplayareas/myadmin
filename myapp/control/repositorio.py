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
from collections import Counter
from myapp.utils.utilidades import Constant

bp = Blueprint("repositorio", __name__, url_prefix="/repositorio")

def delete_json_file(name, usuario_id):
    # Save frequencyOfEachFile in a json file
    singleName = name + ".json"
    user_directory = Constant.PATH_JSON + '/' + str(usuario_id)
    fileName = user_directory + '/' + name + '.json'
    #Delete the user file if exists
    Util.DeleteFileIfExist(fileName)
    print("The file {} was deleted with success!".format( singleName ))

def delete_img_file(name, usuario_id):
    # Save frequencyOfEachFile in a json file
    singleName = name + ".png"
    user_directory = Constant.PATH_IMG + '/' + str(usuario_id)
    fileName = user_directory + '/' + name + '.png'
    #Delete the user file if exists
    Util.DeleteFileIfExist(fileName)
    print("The file {} was deleted with success!".format( singleName ))

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
            user_directory = Constant.PATH_JSON + '/' + str(g.user['id'])
            fileName = user_directory + '/' + name + '.json'
            #Create the user directory if not existe
            Util.CreateDirectoryIfNotExists(user_directory)
            with open(fileName, 'w', encoding="utf-8") as jsonFile:
                json.dump(frequencyOfEachFile, jsonFile)
            print("The file {} was saved with success!".format( singleName ))
        except: 
            print( "Error when try to save the json file")

        print( "Processing word cloud...")
        analysis.generateWordCloud(g.user['id'])

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
    query = "select id, name, link, creation_date, analysis_date, analysed from repository where id = ?"
    repositorio = db.execute( query, (id,) ).fetchone()      
    return repositorio

""" Mostra a lista de repositorios  """
@bp.route("/listar")
@login_required
def listar():
    #Carrega repositorios registrados pelo usuario
    lista_repositorios = lista_repositorios_usuario(g.user["id"])
        
    return render_template("repositorio/listar.html", usuario = g.user['username'], 
            profilePic=g.user['image'], titulo="Repositorios", repositorios=lista_repositorios)

""" Mostra a lista de repositorios  """
@bp.route("/listar")
@login_required
def listar_todos():
    #Carrega repositorios registrados no sistema
    db = get_db()
    query = "SELECT * FROM repository ORDER BY id"
    lista_repositorios = db.execute( query ).fetchall()
        
    return render_template("repositorio/listar.html", usuario = g.user['username'], 
            profilePic=g.user['image'], titulo="Repositorios", repositorios=lista_repositorios)

@bp.route("/criar", methods=["GET", "POST"])
@login_required
def criar():
    """Create a new repository for the current user."""
    if request.method == "POST":
        name = request.form["name"]
        link = request.form["link"]
        error = None
        error_processing_repository = None

        if not name:
            error = "Name is required."

        if not link:
            error = "Link is required."

        if error is not None:
            flash(error, 'danger')
        else:
            # Conecta com o banco para inserir um novo repositorio
            db = get_db()
            query_insert = "INSERT INTO repository (name, link, user_id, creation_date, analysis_date, analysed) VALUES (?, ?, ?, ?, ?, ?)"
            db.execute(
                query_insert,(name, link, g.user["id"], datetime.datetime.now(), datetime.datetime.now(), 1),
            )
            try:
                # Processa o repositorio para gerar a nuvem de arquivos mais modificados
                arquivos = processing(link, name)
            except:
                error_processing_repository = "Erro no processamento da analise do repository."
                if error_processing_repository is not None:
                    flash(error_processing_repository, 'danger')
                    return redirect(url_for("repositorio.listar"))
            db.commit()
            message = "Repositório criado com sucesso!"
            flash(message, 'success')
            return redirect(url_for("repositorio.listar"))

    return render_template("repositorio/criar.html", usuario = g.user['username'], 
            profilePic=g.user['image'], titulo="Repositorios")
        
# Visualiza as informacoes de um dado repositorio selecionado
@bp.route("/<int:id>/visualizar", methods=["GET"])
@login_required
def visualizar(id):    
    # Dados do reposotorio
    repositorio = dados_do_repositorio(id)
    link = repositorio['link']
    name = repositorio['name']
    creation_date = repositorio['creation_date']
    analysis_date = repositorio['analysis_date']
    quantidade_commits = 0
    quantidade_autores = 0
    quantidade_arquivos = 0
    quantidade_tipos = 0
    counter_list_of_types = []

    fileName = Constant.PATH_JSON + '/' + str(g.user['id']) + '/' + name + ".json"

    with open(fileName, 'r', encoding="utf-8") as jsonFile:
        arquivos = dict(json.loads(jsonFile.read()))
        counter_list_of_types = check_tipos_de_arquivos(arquivos)
        arquivos_ordenados = dict( sorted(arquivos.items(), key=lambda item: item[1], reverse=True) )
        counter_list_of_types = dict( sorted( counter_list_of_types.items(), key=lambda item: item[1], reverse=True) )

        quantidade_arquivos = len(arquivos)
        quantidade_tipos = len(counter_list_of_types)

    return render_template("repositorio/visualizar.html", usuario = g.user['username'], usuario_id=str(g.user['id']), 
            profilePic=g.user['image'], titulo="Detalhes do Repositorio", name=name, arquivos=arquivos_ordenados, 
            quantidade_commits=0, quantidade_autores=0, quantidade_arquivos=quantidade_arquivos,quantidade_tipos=quantidade_tipos, 
            lista_tipos=counter_list_of_types, data_criacao=creation_date, data_analises=analysis_date)

# dado um arquivo json convertido em dicionario retorna a lista de extensoes dos arquivos
def check_tipos_de_arquivos(arquivo):
    # Percorre todos os itens do dicionario json
    list_of_types = []
    for key, value in arquivo.items():            
    # Para cada item faz o split por .
        item = key.split('.')
        if len(item)==2: 
            list_of_types.append(item[1])
    return Counter(list_of_types)

@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):    
    """Update a repository if the current user."""
    repository = dados_do_repositorio(id)

    if request.method == "POST":
        name = request.form["name"]
        link = request.form["link"]
        creation_date = request.form["creation_date"]
        analysis_date = request.form["analysis_date"]
        analysed = request.form["analysed"] 
        error = None

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            analysis_date = datetime.datetime.now()
            db = get_db()
            db.execute(
                "UPDATE repository SET name = ?, analysis_date = ? WHERE id = ?", (name, analysis_date, id)
            )
            try:
                # Processa o repositorio para gerar a nuvem de arquivos mais modificados
                arquivos = processing(link, name)
            except:
                error_processing_repository = "Erro no processamento da analise do repository."
                if error_processing_repository is not None:
                    flash(error_processing_repository, 'danger')
                    return redirect(url_for("repositorio.listar"))
            db.commit()
            message = "Repositório atualizado com sucesso!"
            flash(message, 'success')
            return redirect(url_for("repositorio.listar"))

    return render_template("repositorio/update.html", usuario = g.user['username'], 
            profilePic=g.user['image'], titulo="Update Repository", repository=repository)

@bp.route("/<int:id>/delete", methods=["GET"])
@login_required
def delete(id):
    repository = dados_do_repositorio(id)
    name_repository = repository['name']

    db = get_db()
    db.execute("DELETE FROM repository WHERE id = ?", (id,))
    db.commit()
    
    #TODO remover os arquivos img e json do repository correspondente
    delete_img_file(name_repository, g.user['id'])
    delete_json_file(name_repository, g.user['id'])

    message = "Repositório removido com sucesso!"
    flash(message, 'success')
    return redirect(url_for("repositorio.listar"))