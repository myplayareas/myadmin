# myadmin
MyAdmin web application in flask

1. Clonar o repositorio

2. Configurar as variáveis de ambiente
```
export FLASK_APP=myapp
export FLASK_ENV=development
```

3. Reinicializa o db
```
flask init-db
```

4. Roda a aplicação
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