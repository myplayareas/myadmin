# myadmin

MyAdmin is a web application that prototypes some basic analysis of repositories. It uses the pydriller (https://github.com/ishepard/pydriller) to analyze and mining data from software repositories.

It was created using the flask framework (https://flask.palletsprojects.com) and the AdminLTE (Free Bootstrap Admin Template) as UI interation.

1. Clone the repository

2. Configure environment variables
```
export FLASK_APP=myapp
export FLASK_ENV=development
```

3. Restart database
```
flask init-db
```

4. Run application
```
flask run
```

5. Install dependencies
```
pip install pydriller
pip install wordcloud
```

6. Executar os testes da aplicação
```
pip install pytest pytest-html
pip install coverage
cd tests
./my_testes.sh
```

7. Testes funcionais de regressão que devem ser executados: 

7.1 Login (OK)

7.2 Esqueci minha senha

7.3 Registrar um novo usuario

7.4 Checar todos os elementos do dashboard

7.5 Listar membros (OK)

7.6 Lista de repositorios do usuario logado (OK)

7.7 Visualizar detalhes do primeiro repositorio da lista de repositorios

7.8 Checar todos os elementos do repositorio visualizado

7.9 Visualizar profile do usuario 

7.10 Alterar name e email do usuario

7.11 Alterar imagem do usuario

7.12 Criar novo repositorio

7.13 Alterar nome do repositorio

7.14 Deletar repositorio
