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
from myapp.utils.utilidades import Constant

bp = Blueprint("usuario", __name__, url_prefix="/usuario")

""" Mostra a lista de usuarios  """
@bp.route("/listar")
@login_required
def listar():
    #Carrega usuarios registrados no sistema
    db = get_db()
    query = "SELECT * FROM user ORDER BY id"
    lista_usuarios = db.execute( query ).fetchall()
        
    return render_template("usuario/listar.html", usuario = g.user['username'], 
            profilePic=g.user['image'], titulo="Usuários", usuarios=lista_usuarios)

@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):    
    if request.method == "POST":
        username = request.form["username"]
        file_name_to_store = "picture-" + str(id) + ".png" 
        error = None

        if not username:
            error = "Username is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE user SET image = ? WHERE id = ?", (file_name_to_store, id)
            )
            try:
                # Processa o upload do arquivo de imagem
                print('Processamento do upload da imagem')
                # TO DO: isolar o tratamento de arquivo
                file_image = request.files["image"]
                path_to_save = Constant.PATH_UPLOADS + "/" + file_name_to_store
                # Salva o arquivo no diretorio de uploads
                file_image.save(path_to_save)
            except:
                error_processing_upload = "Erro no processamento do upload do processamento da imagem."
                if error_processing_upload is not None:
                    flash(error_processing_upload, 'danger')
                    return redirect(url_for("usuario.listar"))
            db.commit()
            message = "Usuario atualizado com sucesso!"
            flash(message, 'success')
            return redirect(url_for("dashboard.profile"))

    return render_template("usuario/imagem.html", usuario = g.user['username'], 
            profilePic=g.user['image'], titulo="Update image", usuario_logado=g.user)