# myadmin

MyAdmin is a web application that prototypes some basic analysis of repositories. It uses the pydriller (https://github.com/ishepard/pydriller) to analyze and mining data from software repositories.

=======
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

5. Executar os testes da aplicação
```
pip install pytest pytest-html
pip install coverage
cd tests
./my_testes.sh
```

6. Testes funcionais de regressão que devem ser executados: 
6.1 Login (OK)
6.2 Esqueci minha senha
6.3 Registrar um novo usuario
6.4 Checar todos os elementos do dashboard
6.5 Listar membros (OK)
6.6 Lista de repositorios do usuario logado (OK)
6.7 Visualizar detalhes do primeiro repositorio da lista de repositorios
6.8 Checar todos os elementos do repositorio visualizado
6.9 Visualizar profile do usuario 
6.10 Alterar name e email do usuario
6.11 Alterar imagem do usuario
6.12 Criar novo repositorio
6.13 Alterar nome do repositorio
6.14 Deletar repositorio