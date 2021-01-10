# myadmin

MyAdmin is a web application that prototypes some basic analysis of repositories. It uses the pydriller (https://github.com/ishepard/pydriller) to analyze and mining data from software repositories.

It was created using the flask framework (https://flask.palletsprojects.com) and the AdminLTE (Free Bootstrap Admin Template) as UI interation.

1. Clone the repository

2. Configure environment variables
```
export FLASK_APP=myapp
export FLASK_ENV=development
```

3. Configure email client
```
echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env
echo "sendgrid.env" >> .gitignore
source ./sendgrid.env
```

4. Install dependencies
```
pip install pydriller
pip install wordcloud
pip install sendgrid
```

5. Restart database
```
flask init-db
```

6. Run application
```
flask run
```

7. Executar os testes da aplicação
```
pip install pytest pytest-html
pip install coverage
cd tests
./my_testes.sh
```

8. Testes funcionais de regressão que devem ser executados: 

8.1 Login (OK)

8.2 Esqueci minha senha

8.3 Registrar um novo usuario

8.4 Checar todos os elementos do dashboard

8.5 Listar membros (OK)

8.6 Lista de repositorios do usuario logado (OK)

8.7 Visualizar detalhes do primeiro repositorio da lista de repositorios

8.8 Checar todos os elementos do repositorio visualizado

8.9 Visualizar profile do usuario 

8.10 Alterar name e email do usuario

8.11 Alterar imagem do usuario

8.12 Criar novo repositorio

8.13 Visualizar repositorio criado

8.14 Alterar nome do repositorio

8.15 Deletar repositorio
