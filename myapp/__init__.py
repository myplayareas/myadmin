import os
from flask import Flask
# register the database commands
from myapp.config import db
# apply the blueprints to the app
from myapp.control import auth
from myapp.control import dashboard
from myapp.control import usuario
from myapp.control import repositorio
from myapp.control import dashboardmetrics
from myapp.utils.utilidades import Constant
import ssl # para garantir o request https do notebook da máquina cliente
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import nexmo
import datetime

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "myapp.sqlite"),
    )
    # cria um contexto para chamadas do request https da máquina cliente
    ssl._create_default_https_context = ssl._create_unverified_context

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def dados_da_alicacao():
        print('Diretorio da app: {}'. format(os.path.dirname(app.instance_path)))    
        print('Myapp path: {}'.format(app.root_path))
        print('App instance path: {}'.format(app.instance_path))
        print('')
        print('myadmin: {}'.format(Constant.PATH_MYADMIN))
        print('myapp: {}'.format(Constant.PATH_MYAPP))
        print('static: {}'.format(Constant.PATH_STATIC))
        print('uploads: {}'.format(Constant.PATH_UPLOADS))
        print('img: {}'.format(Constant.PATH_IMG))
        print('json: {}'.format(Constant.PATH_JSON))    

    @app.route("/myapp")
    def hello():
        dados_da_alicacao()
        return "Aplicacao Web Python usando Flask"

    @app.route("/sobre")
    def about():
        dados_da_alicacao()
        return "Aplicacao Web Python usando Flask"

    @app.route("/email")
    def email():
        if (os.environ.get('SENDGRID_API_KEY') is None):
            return "A variável de ambiente SENDGRID_API_KEY não foi definida!"

        message = Mail(from_email='armando@ufpi.edu.br',to_emails='armando.sousa@gmail.com',
        subject='Mensagem enviada pelo Myaap',
        html_content='<strong>Esta é uma mensagem de teste enviada pela aplicação MyApp</strong>')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
        return "E-mail enviado com sucesso!"

    # nexmo
    @app.route("/sms")
    def sms():
        if (os.environ.get('NEXMO_KEY') is None):
            return "A variável de ambiente NEXMO_KEY não foi definida!"

        try:
            client = nexmo.Client(key=os.environ.get('NEXMO_KEY') , secret=os.environ.get('NEXMO_SECRET'))

            data = datetime.datetime.now()
            mensagem = 'SMS API from Myapp. ' + str(data) + ' by Armando Soares'
            client.send_message({
                'from': 'Vonage APIs',
                'to': '5586994693558',
                'text': mensagem,
            })      
            print('SMS enviado com sucesso as {}'.format(datetime.datetime.now()))
        except Exception as e:
            print(e.message)
        return "SMS enviado com sucesso!"

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(usuario.bp)
    app.register_blueprint(repositorio.bp)
    app.register_blueprint(dashboardmetrics.bp)

    # Define a rota principal da aplicacao
    app.add_url_rule("/", endpoint="index")

    return app