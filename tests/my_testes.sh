#!/bin/bash      
echo "Executa os testes do Myapp"

echo "Executa os testes da suite de testes test_myadmin"
pytest -v test_myadmin.py --html=pytest_report_test_myadmin.html --self-contained-html 
echo "Executa os testes da suite de testes test_utilities"
pytest -v test_utilities.py --html=pytest_report_test_utilities.html --self-contained-html
echo "Executa os testes da suite de testes test_check_commits"
pytest -v test_check_commits.py --html=pytest_report_test_check_commits.html --self-contained-html
echo "Faz a analise de cobertura da aplicacao myapp"
coverage run -m pytest
coverage html
